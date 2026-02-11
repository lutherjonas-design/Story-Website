import { Link } from 'react-router-dom'
import "./Navbar.css"

export default function Navbar() {
  return (
    <header className="navbar">
      <nav>
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/stories">Stories</Link></li>
          <li><Link to="/dictionary">Dictionary</Link></li>
        </ul>
      </nav>
    </header>
  )
}
