import { useState } from 'react'
import PortfolioModal from './PortfolioModal'
import TechStack from './TechStack'
import '../styles/FloatingButton.css'

export default function FloatingButton() {
  const [showPortfolio, setShowPortfolio] = useState(false)
  const [showTechStack, setShowTechStack] = useState(false)
  const [showMenu, setShowMenu] = useState(false)

  const handleDocClick = () => {
    window.open('http://localhost:8000/docs', '_blank')
    setShowMenu(false)
  }

  const handlePortfolioClick = () => {
    setShowPortfolio(true)
    setShowMenu(false)
  }

  const handleTechStackClick = () => {
    setShowTechStack(true)
    setShowMenu(false)
  }

  return (
    <>
      <PortfolioModal isOpen={showPortfolio} onClose={() => setShowPortfolio(false)} />
      <TechStack isOpen={showTechStack} onClose={() => setShowTechStack(false)} />
      
      <div className="floating-menu">
        {showMenu && (
          <>
            <button 
              id="floating-docs-btn"
              data-testid="floating-docs-btn"
              className="floating-menu-item docs-btn" 
              onClick={handleDocClick}
            >
              📚 API Docs
            </button>
            <button 
              id="floating-portfolio-btn"
              data-testid="floating-portfolio-btn"
              className="floating-menu-item portfolio-btn" 
              onClick={handlePortfolioClick}
            >
              👩‍💻 Portfólio
            </button>
            <button 
              id="floating-tech-btn"
              data-testid="floating-tech-btn"
              className="floating-menu-item tech-btn" 
              onClick={handleTechStackClick}
            >
              ⚙️ Tecnologias
            </button>
          </>
        )}
        <button 
          id="floating-button"
          data-testid="floating-button"
          className={`floating-button ${showMenu ? 'active' : ''}`} 
          onClick={() => setShowMenu(!showMenu)}
        >
          ✨
        </button>
      </div>
    </>
  )
}
