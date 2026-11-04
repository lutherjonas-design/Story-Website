import { Link } from 'react-router-dom'
import "./Navbar.css"
import { ThemeToggle } from "./ThemeToggle";

export default function Navbar() {
  return (
    <header className="navbar">
      <nav className="nav-inner">
        <ul className="nav-links">
          <li><Link to="/">Home</Link></li>
          <li><Link to="/stories">Stories</Link></li>
          <li><Link to="/dictionary">Dictionary</Link></li>
        </ul>

        <div className="nav-actions">
          <ThemeToggle />
        </div>
      </nav>
    </header>
  )
}