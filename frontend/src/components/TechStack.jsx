import '../styles/TechStack.css'

export default function TechStack({ isOpen, onClose }) {
  if (!isOpen) return null

  const technologies = [
    {
      category: "Frontend",
      items: [
        { name: "React 18", icon: "⚛️", description: "Biblioteca JavaScript para UI" },
        { name: "Vite", icon: "⚡", description: "Build tool rápido e moderno" },
        { name: "CSS3", icon: "🎨", description: "Estilização e design responsivo" },
        { name: "Axios", icon: "🔗", description: "Cliente HTTP para requisições" }
      ]
    },
    {
      category: "Backend",
      items: [
        { name: "Python", icon: "🐍", description: "Linguagem de programação" },
        { name: "FastAPI", icon: "⚙️", description: "Framework web moderno" },
        { name: "SQLAlchemy", icon: "🗄️", description: "ORM para banco de dados" },
        { name: "PostgreSQL", icon: "🐘", description: "Banco de dados relacional" }
      ]
    },
    {
      category: "Autenticação & Segurança",
      items: [
        { name: "Bcrypt", icon: "🔐", description: "Hash seguro de senhas" },
        { name: "CORS", icon: "🛡️", description: "Controle de acesso entre domínios" },
        { name: "Pydantic", icon: "✅", description: "Validação de dados" }
      ]
    },
    {
      category: "Ferramentas & Deploy",
      items: [
        { name: "Git", icon: "📦", description: "Controle de versão" },
        { name: "npm", icon: "📥", description: "Gerenciador de pacotes" },
        { name: "Swagger", icon: "📚", description: "Documentação de API" }
      ]
    }
  ]

  return (
    <div id="techstack-overlay" data-testid="techstack-overlay" className="techstack-overlay">
      <div id="techstack-modal" data-testid="techstack-modal" className="techstack-modal">
        <button 
          id="techstack-close"
          data-testid="techstack-close"
          className="techstack-close"
          onClick={onClose}
        >
          ✕
        </button>

        <div className="techstack-header">
          <h1>⚙️ Tecnologias Usadas</h1>
          <p>Stack completo da aplicação Mybookie</p>
        </div>

        <div className="techstack-content">
          {technologies.map((tech, idx) => (
            <div key={idx} className="tech-category">
              <h2>{tech.category}</h2>
              <div className="tech-items">
                {tech.items.map((item, i) => (
                  <div key={i} className="tech-item">
                    <span className="tech-icon">{item.icon}</span>
                    <div className="tech-info">
                      <h3>{item.name}</h3>
                      <p>{item.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}

          <div className="tech-summary">
            <h2>📊 Resumo</h2>
            <ul>
              <li>✅ Full-stack moderna</li>
              <li>✅ API RESTful com documentação automática</li>
              <li>✅ Autenticação com hash bcrypt</li>
              <li>✅ Banco de dados relacional PostgreSQL</li>
              <li>✅ Frontend responsivo e interativo</li>
              <li>✅ IDs únicos para automação de testes</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}