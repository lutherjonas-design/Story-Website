import { useState, useEffect } from "react";
import "./ThemeToggle.css"

export function ThemeToggle() {
    const [theme, setTheme] = useState(() => {
        // read from localStorage or default to light
        return localStorage.getItem("theme") || "light";
    });

    useEffect(() => {
        const root = document.documentElement;

        if (theme === "dark") {
            root.setAttribute("data-theme", "dark");
        } else {
            root.removeAttribute("data-theme");
        }

        localStorage.setItem("theme", theme);
    }, [theme]);


    return (
        <button
            onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
            className="theme-toggle"
            aria-label={theme === 'light' ? 'Switch to dark mode' : 'Switch to light mode'}
        >
            {theme === 'light' ? '🌙' : '☀'}
        </button>
    )
}

