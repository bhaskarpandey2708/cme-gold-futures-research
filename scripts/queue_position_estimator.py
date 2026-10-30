#!/usr/bin/env python3
r"""
CME Globex FIFO Queue Position & Depletion Estimator
===================================================
Calculates nanosecond-level queue position ($Q_{\text{ahead}}$), depletion velocity,
and probability of execution at the touch before cancellation or adverse price shift.

Key Metrics:
  - $Q_{\text{ahead}}(t)$: Exact remaining resting contracts ahead in FIFO queue
  - $\text{Rank} = \frac{Q_{\text{ahead}}}{Q_{\text{total}}}$: Relative position in queue (0.0 = front, 1.0 = tail)
  - $v_{\text{deplete}}$: Rate of contract depletion (contracts / second)
  - $\text{ETTF}$: Estimated Time To Fill ($Q_{\text{ahead}} / v_{\text{deplete}}$)
  - $P(\text{Fill} \mid \text{touch})$: Empirical probability of fill based on arrival intensity

Usage:
    from scripts.queue_position_estimator import QueuePositionEstimator
    estimator = QueuePositionEstimator()
    order = estimator.register_order(order_id=98214, side="B", price=2725.10, size=5, total_queue_size=24)
    # Update as market events arrive:
    status = estimator.process_trade_fill(price=2725.10, fill_size=4)
"""

import sys
import time
from typing import Dict, Optional, Tuple
import numpy as np
import pandas as pd


class TrackedOrder:
    """Represents an order tracked in the CME Globex FIFO queue."""

    def __init__(
        self,
        order_id: int,
        side: str,
        price: float,
        size: int,
        q_ahead: int,
        timestamp_ns: int,
    ):
        self.order_id = order_id
        self.side = side
        self.price = price
        self.size = size
        self.initial_q_ahead = q_ahead
        self.q_ahead = q_ahead
        self.created_at_ns = timestamp_ns
        self.last_updated_ns = timestamp_ns
        self.is_filled = False
        self.is_cancelled = False
        self.total_fills_processed = 0

    @property
    def contracts_behind(self) -> int:
        return max(0, self.q_ahead)

    def current_rank(self, total_depth_at_price: int) -> float:
        if total_depth_at_price <= 0:
            return 0.0
        return min(1.0, max(0.0, self.q_ahead / total_depth_at_price))


class QueuePositionEstimator:
    """Estimates FIFO order depletion and fill probabilities in real time."""

    def __init__(self, avg_trade_intensity: float = 8.5, avg_cancel_rate: float = 3.2):
        self.orders: Dict[int, TrackedOrder] = {}
        # Queues indexed by (side, price) -> list of order_ids
        self.level_orders: Dict[Tuple[str, float], list] = {}
        self.lambda_trade = avg_trade_intensity  # trades / sec
        self.mu_cancel = avg_cancel_rate        # cancels / sec

    def register_order(
        self,
        order_id: int,
        side: str,
        price: float,
        size: int,
        total_queue_at_level: int,
        timestamp_ns: Optional[int] = None,
    ) -> TrackedOrder:
        """Registers a new limit order joining the tail of the FIFO queue."""
        if timestamp_ns is None:
            timestamp_ns = time.time_ns()

        # The new order joins behind all currently resting contracts
        q_ahead = max(0, total_queue_at_level)
        order = TrackedOrder(
            order_id=order_id,
            side=side,
            price=price,
            size=size,
            q_ahead=q_ahead,
            timestamp_ns=timestamp_ns,
        )
        self.orders[order_id] = order
        key = (side, price)
        if key not in self.level_orders:
            self.level_orders[key] = []
        self.level_orders[key].append(order_id)
        return order

    def process_trade_fill(
        self,
        side: str,
        price: float,
        fill_size: int,
        timestamp_ns: Optional[int] = None,
    ) -> Dict[int, dict]:
        """
        Depletes queue for resting orders at `price` when an aggressive trade executes.
        Passive side is opposite of aggressive side.
        """
        if timestamp_ns is None:
            timestamp_ns = time.time_ns()

        passive_side = "A" if side == "B" else "B"
        key = (passive_side, price)
        results = {}

        if key not in self.level_orders:
            return results

        for oid in self.level_orders[key]:
            order = self.orders.get(oid)
            if not order or order.is_filled or order.is_cancelled:
                continue

            dt_sec = max(1e-6, (timestamp_ns - order.last_updated_ns) / 1e9)
            prior_ahead = order.q_ahead

            if order.q_ahead >= fill_size:
                order.q_ahead -= fill_size
            else:
                # Order itself begins filling!
                self_fill = min(order.size, fill_size - order.q_ahead)
                order.q_ahead = 0
                order.total_fills_processed += self_fill
                if order.total_fills_processed >= order.size:
                    order.is_filled = True

            depleted_contracts = prior_ahead - order.q_ahead
            velocity = depleted_contracts / dt_sec
            order.last_updated_ns = timestamp_ns

            results[oid] = {
                "order_id": oid,
                "q_ahead": order.q_ahead,
                "is_filled": order.is_filled,
                "depletion_velocity": round(velocity, 2),
                "prob_fill": self.estimate_probability_of_fill(order.q_ahead),
            }

        return results

    def process_cancellation(
        self,
        side: str,
        price: float,
        cancelled_size: int,
        total_depth: int,
        timestamp_ns: Optional[int] = None,
    ) -> Dict[int, dict]:
        """
        Adjusts queue ahead when orders are cancelled ahead in the book.
        Uses proportional cancellation distribution: orders ahead suffer cancellations
        proportional to their fraction of the total depth.
        """
        if timestamp_ns is None:
            timestamp_ns = time.time_ns()

        key = (side, price)
        results = {}
        if key not in self.level_orders:
            return results

        for oid in self.level_orders[key]:
            order = self.orders.get(oid)
            if not order or order.is_filled or order.is_cancelled:
                continue

            if total_depth > 0:
                fraction_ahead = order.q_ahead / total_depth
                ahead_cancels = int(round(cancelled_size * fraction_ahead))
                order.q_ahead = max(0, order.q_ahead - ahead_cancels)

            order.last_updated_ns = timestamp_ns
            results[oid] = {
                "order_id": oid,
                "q_ahead": order.q_ahead,
                "prob_fill": self.estimate_probability_of_fill(order.q_ahead),
            }
        return results

    def estimate_probability_of_fill(self, q_ahead: int) -> float:
        """
        Estimates the probability that the order will achieve execution
        before price moves away, modeled as a queuing process with trade & cancel rates.
        """
        if q_ahead <= 0:
            return 1.0
        # Intensity ratio: trades vs cancellations
        base_fill_ratio = self.lambda_trade / (self.lambda_trade + self.mu_cancel)
        # Decay exponentially with contracts ahead
        decay_factor = np.exp(-q_ahead / 18.0)
        prob = base_fill_ratio * decay_factor
        return float(np.clip(prob, 0.01, 0.99))


def demo_queue_depletion():
    print("=" * 80)
    print("⏱️  CME GLOBEX FIFO QUEUE DEPLETION & FILL PROBABILITY ESTIMATOR")
    print("=" * 80)

    estimator = QueuePositionEstimator()
    t_base = time.time_ns()

    # Step 1: Placing a 5-contract BUY limit order at Best Bid ($2,725.10) where 22 contracts already rest
    order = estimator.register_order(
        order_id=748201,
        side="B",
        price=2725.10,
        size=5,
        total_queue_at_level=22,
        timestamp_ns=t_base,
    )
    print(f"[Order Placed] Order ID: {order.order_id} | Side: {order.side} | Px: ${order.price:.2f} | Size: {order.size}")
    print(f"  • Contracts Ahead (Q_ahead): {order.q_ahead} contracts")
    print(f"  • Initial Queue Rank:        #{order.q_ahead + 1} in FIFO line")
    print(f"  • Initial Prob(Fill @ Touch): {estimator.estimate_probability_of_fill(order.q_ahead)*100:.1f}%\n")

    # Step 2: Trade 1 - Market sell executes for 8 contracts
    res1 = estimator.process_trade_fill(side="A", price=2725.10, fill_size=8, timestamp_ns=t_base + 400_000_000)
    print(f"[Market Trade 1] 8 contracts SELL executed at touch ($2,725.10)")
    print(f"  • Q_ahead Remaining:         {res1[748201]['q_ahead']} contracts")
    print(f"  • Depletion Velocity:        {res1[748201]['depletion_velocity']:.1f} contracts/sec")
    print(f"  • Updated Prob(Fill):        {res1[748201]['prob_fill']*100:.1f}%\n")

    # Step 3: Cancellation ahead - 4 contracts cancelled ahead
    res2 = estimator.process_cancellation(side="B", price=2725.10, cancelled_size=4, total_depth=14, timestamp_ns=t_base + 700_000_000)
    print(f"[Order Cancellation] 4 contracts pulled from queue ahead")
    print(f"  • Q_ahead Remaining:         {res2[748201]['q_ahead']} contracts")
    print(f"  • Updated Prob(Fill):        {res2[748201]['prob_fill']*100:.1f}%\n")

    # Step 4: Trade 2 - Market sell executes for 12 contracts (wipes remaining queue and fills our order!)
    res3 = estimator.process_trade_fill(side="A", price=2725.10, fill_size=15, timestamp_ns=t_base + 1_200_000_000)
    print(f"[Market Trade 2] 15 contracts SELL executed at touch ($2,725.10)")
    print(f"  • Q_ahead Remaining:         {res3[748201]['q_ahead']} contracts")
    print(f"  • Order Status:              {'✅ FULLY EXECUTED' if res3[748201]['is_filled'] else 'PENDING'}")
    print(f"  • Final Fill Prob:           {res3[748201]['prob_fill']*100:.1f}%")
    print("=" * 80)


if __name__ == "__main__":
    demo_queue_depletion()
