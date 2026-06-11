import { useState, useEffect } from 'react'
import Auth from './components/Auth'
import Navigation from './components/Navigation'
import BookList from './components/BookList'
import About from './components/About'
import FloatingButton from './components/FloatingButton'
import './App.css'

function App() {
  const [user, setUser] = useState(null)
  const [currentPage, setCurrentPage] = useState('books')

  useEffect(() => {
    // Verificar se existe usuário no localStorage
    const savedUser = localStorage.getItem('user')
    if (savedUser) {
      setUser(JSON.parse(savedUser))
    }
  }, [])

  const handleLoginSuccess = (userData) => {
    setUser(userData)
    setCurrentPage('books')
  }

  const handleLogout = () => {
    localStorage.removeItem('user')
    setUser(null)
    setCurrentPage('books')
  }

  if (!user) {
    return (
      <>
        <Auth onLoginSuccess={handleLoginSuccess} />
        <FloatingButton />
      </>
    )
  }

  return (
    <div className="App">
      <Navigation 
        user={user} 
        currentPage={currentPage}
        setCurrentPage={setCurrentPage}
        onLogout={handleLogout}
      />
      
      <FloatingButton />
      
      <main className="main-content">
        {currentPage === 'books' && <BookList />}
        {currentPage === 'about' && <About />}
      </main>
    </div>
  )
}

export default App