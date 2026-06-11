import '../styles/Navigation.css'

export default function Navigation({ user, currentPage, setCurrentPage, onLogout }) {
  return (
    <nav id="navigation" data-testid="navigation" className="navbar">
      <div id="nav-container" data-testid="nav-container" className="nav-container">
        <div id="nav-logo" data-testid="nav-logo" className="nav-logo">
          📚 Mybookie
        </div>

        <div id="nav-links" data-testid="nav-links" className="nav-links">
          <button
            id="nav-btn-books"
            data-testid="nav-btn-books"
            className={`nav-btn ${currentPage === 'books' ? 'active' : ''}`}
            onClick={() => setCurrentPage('books')}
          >
            📚 Livros
          </button>
          <button
            id="nav-btn-about"
            data-testid="nav-btn-about"
            className={`nav-btn ${currentPage === 'about' ? 'active' : ''}`}
            onClick={() => setCurrentPage('about')}
          >
            ℹ️ Sobre
          </button>
        </div>

        <div id="nav-user-info" data-testid="nav-user-info" className="nav-user-info">
          <span id="nav-username" data-testid="nav-username">{user?.username}</span>
          <button
            id="nav-btn-logout"
            data-testid="nav-btn-logout"
            className="nav-btn logout"
            onClick={onLogout}
          >
            🚪 Sair
          </button>
        </div>
      </div>
    </nav>
  )
}