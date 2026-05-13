import io
import sqlite3
from datetime import datetime, timezone, timedelta
import os
import matplotlib.pyplot as plt
import requests
from PIL import Image


class Coin:
    """Represents a single cryptocurrency and provides price/graph utilities."""

    def __init__(self, coin_id: str, coin_name: str = None, coin_img_url: str = None, price: float = None):
        self.coin_id = coin_id
        self.coin_name = coin_name
        self.coin_img_url = coin_img_url
        self._cached_price = price

        if coin_name is None and coin_id != "EUR":
            
            with sqlite3.connect("cryptodata.sqlite") as conn:
                row = conn.execute(
                    "SELECT coin_name, coin_img FROM coins WHERE coin_id = ?", (coin_id,)
                ).fetchone()
            self.coin_name = row[0]
            self.coin_img_url = row[1]

    # ------------------------------------------------------------------
    # Price queries
    # ------------------------------------------------------------------

    def get_price_history(self) -> dict[str, float]:
        """Returns {date: price} for all available dates."""
        
        with sqlite3.connect("cryptodata.sqlite") as conn:
            cur = conn.cursor()
            rows = cur.execute(
                "SELECT date, price FROM coins_prices WHERE coin_id = ?",
                (self.coin_id,),
            ).fetchall()
        return {date: price for date, price in rows}

    def get_todays_price(self) -> float:
        """Returns the most recent recorded price for this coin."""
        if self._cached_price is not None:
            return self._cached_price
            # fallback to DB if not cached
        
        with sqlite3.connect("cryptodata.sqlite") as conn:
            return conn.execute(
                "SELECT price FROM coins_prices "
                "WHERE coin_id = ? AND date = (SELECT MAX(date) FROM coins_prices WHERE coin_id = ?)",
                (self.coin_id, self.coin_id),
            ).fetchone()[0]

    def get_daily_change_pct(self) -> float:
        """Returns price change percentage vs. yesterday."""
        today_price = self.get_todays_price()
        yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
        
        with sqlite3.connect("cryptodata.sqlite") as conn:
            cur = conn.cursor()
            yesterday_price = cur.execute(
                "SELECT price FROM coins_prices WHERE coin_id = ? AND date = ?",
                (self.coin_id, yesterday),
            ).fetchone()[0]
        return (today_price / yesterday_price) * 100 - 100

    # ------------------------------------------------------------------
    # Metadata accessors
    # ------------------------------------------------------------------

    def get_coin_id(self) -> str:
        return self.coin_id

    def get_coin_name(self) -> str:
        return self.coin_name

    def get_coin_img_url(self) -> str:
        return self.coin_img_url

    def get_coin_image(self) -> Image.Image:
        """Downloads and returns the coin logo as a PIL Image."""
        return Image.open(io.BytesIO(requests.get(self.coin_img_url).content))

    # ------------------------------------------------------------------
    # Graph
    # ------------------------------------------------------------------

    def save_graph(self) -> None:
        """Renders a price chart and saves it to temp/<coin_id>.png."""
        if "temp" not in os.listdir():
            os.mkdir("temp")
        elif f"temp/{self.coin_id}.png" in os.listdir("temp"):
            return  # Skip if already saved
        history = self.get_price_history()
        dates = list(history.keys())
        prices = list(history.values())

        fig, ax = plt.subplots(figsize=(15, 7))
        fig.set_facecolor("#0b0e11")
        ax.set_facecolor("#0b0e11")

        ax.set_xticks(range(0, len(dates), max(len(dates) // 12, 1)))
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (EUR)")

        for element in (ax.xaxis.label, ax.yaxis.label):
            element.set_color("white")
        ax.tick_params(axis="both", colors="white")
        for spine in ax.spines.values():
            spine.set_color("white")

        # Build error bars: green for up days, red for down days
        up_err, down_err = [], []
        for i in range(len(prices) - 1):
            diff = prices[i + 1] - prices[i]
            if diff > 0:
                up_err.append(0)
                down_err.append(diff)
            else:
                up_err.append(-diff)
                down_err.append(0)

        ax.errorbar(
            dates[:-1], prices[:-1],
            yerr=[up_err, down_err],
            color="lightgreen",
            ecolor="orangered",
        )

        # Coin logo inset
        ax_img = fig.add_axes([0.9, 0.9, 0.1, 0.1])
        ax_img.imshow(self.get_coin_image())
        ax_img.axis("off")

        latest_price = prices[-1]
        best_price = max(prices)
        pct_from_best = (best_price / latest_price) * 100

        ax.text(
            1.01, 0.90,
            f"Latest price\n{round(latest_price, 6)}\n-{round(pct_from_best, 2)}% from best",
            transform=ax.transAxes, color="red",
        )
        ax.text(
            1.01, 0.80,
            f"Best price\n{round(best_price, 6)}",
            transform=ax.transAxes, color="green",
        )

        plt.savefig(f"temp/{self.coin_id}.png", bbox_inches="tight", facecolor=fig.get_facecolor())
        plt.close()

    def show_graph(self) -> None:
        """Saves and opens the price chart."""
        self.save_graph()
        Image.open(f"temp/{self.coin_id}.png").show()
