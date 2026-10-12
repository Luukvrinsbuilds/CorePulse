
import customtkinter as ctk
import psutil

from monitor import get_system_info, get_live_stats


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class CorePulse(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CorePulse")
        self.geometry("900x600")
        self.minsize(700, 500)

        self.configure(fg_color="#10141D")

        # Header
        ctk.CTkLabel(
            self,
            text="COREPULSE",
            font=("Segoe UI", 30, "bold"),
            text_color="#54B8FF"
        ).pack(pady=(25, 0))

        info = get_system_info()

        ctk.CTkLabel(
            self,
            text=f"{info['os']}  |  "
                 f"{info['cores']} cores  |  "
                 f"{info['total_ram']} GB RAM",
            text_color="#AAB4C5"
        ).pack(pady=(5, 20))

        # Dashboard cards
        cards = ctk.CTkFrame(
            self, fg_color="transparent"
        )
        cards.pack(fill="x", padx=20)

        self.labels = {}

        for key, title in [
            ("cpu", "CPU USAGE"),
            ("ram", "RAM USAGE"),
            ("disk", "DISK USAGE"),
        ]:
            card = ctk.CTkFrame(
                cards,
                corner_radius=15,
                fg_color="#1B2230"
            )
            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=7
            )

            ctk.CTkLabel(
                card,
                text=title,
                font=("Segoe UI", 14, "bold"),
                text_color="#AAB4C5"
            ).pack(pady=(20, 8))

            value = ctk.CTkLabel(
                card,
                text="--%",
                font=("Segoe UI", 32, "bold"),
                text_color="#54B8FF"
            )
            value.pack(pady=(0, 5))

            progress = ctk.CTkProgressBar(
                card,
                width=150,
                progress_color="#269DFF"
            )
            progress.pack(padx=15, pady=(5, 20))
            progress.set(0)

            self.labels[key] = (value, progress)

        # Extra system information
        self.details = ctk.CTkLabel(
            self,
            text="Starting monitoring...",
            font=("Consolas", 14),
            text_color="#AAB4C5"
        )
        self.details.pack(pady=35)

        self.status = ctk.CTkLabel(
            self,
            text="● SYSTEM ONLINE",
            text_color="#50D890",
            font=("Segoe UI", 12, "bold")
        )
        self.status.pack(side="bottom", pady=20)

        # Prepare CPU measurement
        psutil.cpu_percent(interval=None)
        self.update_dashboard()

    def update_dashboard(self):
        stats = get_live_stats()

        for key in ("cpu", "ram", "disk"):
            value, progress = self.labels[key]
            percent = stats[key]

            value.configure(text=f"{percent:.1f}%")
            progress.set(percent / 100)

        self.details.configure(
            text=(
                f"RAM: {stats['ram_used']} GB used\n"
                f"Free storage: {stats['disk_free']} GB"
            )
        )

        self.after(1000, self.update_dashboard)


if __name__ == "__main__":
    app = CorePulse()
    app.mainloop()
