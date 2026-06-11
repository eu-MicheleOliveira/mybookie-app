import { useState, useEffect } from 'react'
import '../styles/PortfolioModal.css'

export default function PortfolioModal({ isOpen, onClose }) {
  const [activeTab, setActiveTab] = useState('sobre')

  const portfolioData = {
    nome: "Michele Caroline Teixeira de Oliveira",
    titulo: "Senior QA Engineer | Professora Universitária",
    descricao: "QA Sênior com +7 anos de experiência em Testes de Software",
    email: "michele564000@gmail.com",
    telefone: "(14) 99631-2027",
    linkedin: "https://linkedin.com/in/michelecarolineoliveira",
    
    sobre: {
      descricao: "QA Sênior e Professora universitária com +7 anos de experiência em Testes de Software, atuando na garantia da qualidade em aplicações web e APIs.",
      resumo: [
        "🧪 Senior QA Engineer com 7+ anos",
        "👨‍🏫 Professora de Testes e Qualidade",
        "🤖 Especialista em Automação de Testes",
        "📊 Certificada CTFL",
        "🔄 Especialista em CI/CD"
      ]
    },
    
    skills: [
      { categoria: "Testes & QA", items: ["Automação de Testes", "Testes de API", "BDD", "Cucumber"] },
      { categoria: "Linguagens", items: ["Selenium", "Capybara", "Ruby", "JavaScript"] },
      { categoria: "Metodologias", items: ["CI/CD", "Scrum", "Quality Strategy", "Agile"] }
    ],
    
    experiencia: [
      { titulo: "Professora Universitária", empresa: "Universidade de Marília", periodo: "2025 - Presente" },
      { titulo: "Analista de Testes III", empresa: "Tray", periodo: "2025 - Presente" },
      { titulo: "QA Sênior", empresa: "Tray", periodo: "2020 - 2025" }
    ],
    
    certificacoes: [
      "Certified Tester Foundation Level",
      "Selenium: Testes automatizados",
      "Automação com Capybara e Ruby",
      "Jasmine: Testes em JavaScript"
    ]
  }

  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden'
    }
    return () => {
      document.body.style.overflow = 'unset'
    }
  }, [isOpen])

  if (!isOpen) return null

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        
        {/* FECHAR */}
        <button className="modal-close" onClick={onClose}>✕</button>

        {/* HEADER MINI */}
        <div className="modal-header">
          <div className="modal-avatar">👩‍💻</div>
          <div className="modal-header-info">
            <h2>{portfolioData.nome}</h2>
            <p>{portfolioData.titulo}</p>
          </div>
        </div>

        {/* TABS MINI */}
        <div className="modal-tabs">
          <button 
            className={`modal-tab ${activeTab === 'sobre' ? 'active' : ''}`}
            onClick={() => setActiveTab('sobre')}
          >
            Sobre
          </button>
          <button 
            className={`modal-tab ${activeTab === 'skills' ? 'active' : ''}`}
            onClick={() => setActiveTab('skills')}
          >
            Skills
          </button>
          <button 
            className={`modal-tab ${activeTab === 'exp' ? 'active' : ''}`}
            onClick={() => setActiveTab('exp')}
          >
            Experiência
          </button>
          <button 
            className={`modal-tab ${activeTab === 'cert' ? 'active' : ''}`}
            onClick={() => setActiveTab('cert')}
          >
            Certificações
          </button>
        </div>

        {/* CONTEÚDO */}
        <div className="modal-body">
          
          {activeTab === 'sobre' && (
            <div className="modal-tab-content">
              <p className="modal-desc">{portfolioData.sobre.descricao}</p>
              <div className="modal-highlights">
                {portfolioData.sobre.resumo.map((item, idx) => (
                  <div key={idx} className="highlight-item">{item}</div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'skills' && (
            <div className="modal-tab-content">
              {portfolioData.skills.map((skill, idx) => (
                <div key={idx} className="skill-section">
                  <h4>{skill.categoria}</h4>
                  <div className="modal-skill-items">
                    {skill.items.map((item, i) => (
                      <span key={i} className="modal-skill-badge">{item}</span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'exp' && (
            <div className="modal-tab-content">
              {portfolioData.experiencia.map((exp, idx) => (
                <div key={idx} className="modal-exp-item">
                  <h4>{exp.titulo}</h4>
                  <p className="modal-empresa">{exp.empresa}</p>
                  <p className="modal-periodo">{exp.periodo}</p>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'cert' && (
            <div className="modal-tab-content">
              <div className="modal-cert-list">
                {portfolioData.certificacoes.map((cert, idx) => (
                  <div key={idx} className="modal-cert-item">
                    <span className="cert-icon">✅</span>
                    <span>{cert}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* CONTATO */}
        <div className="modal-footer">
          <p>Conecte-se comigo:</p>
          <div className="modal-contact">
            <a href={`mailto:${portfolioData.email}`} className="modal-contact-btn">
              📧 Email
            </a>
            <a href={`tel:${portfolioData.telefone}`} className="modal-contact-btn">
              📱 Telefone
            </a>
            <a href={portfolioData.linkedin} target="_blank" rel="noopener noreferrer" className="modal-contact-btn">
              💼 LinkedIn
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}
