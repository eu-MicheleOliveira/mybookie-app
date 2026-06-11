import { useState } from 'react'
import '../styles/About.css'

export default function About() {
  const [activeTab, setActiveTab] = useState('sobre')

  const portfolioData = {
    nome: "Michele Caroline Teixeira de Oliveira",
    titulo: "Senior QA Engineer | Professora Universitária | Test Automation",
    descricao: "QA Sênior com +7 anos de experiência em Testes de Software",
    locacao: "Garça, São Paulo, Brasil",
    email: "michele564000@gmail.com",
    telefone: "(14) 99631-2027",
    linkedin: "https://linkedin.com/in/michelecarolineoliveira",
    github: "https://github.com/seu-usuario",
    
    sobre: {
      descricao: "QA Sênior e Professora universitária, com +7 anos de experiência em Testes de Software, atuando na garantia da qualidade em aplicações web e APIs. Pós-graduada em Testes e Desenvolvimento de Software, com foco em automação de testes, qualidade de processos e aprendizado contínuo. Professora na área de Testes e Qualidade de Software, com paixão por compartilhar conhecimento e formar novos profissionais de tecnologia.",
      resumo: [
        "🧪 Senior QA Engineer com 7+ anos de experiência",
        "👨‍🏫 Professora Universitária de Testes e Qualidade de Software",
        "🤖 Especialista em Automação de Testes (Web & API)",
        "📊 Certificada CTFL - Certified Tester Foundation Level",
        "🔄 Especialista em CI/CD e Quality Strategy"
      ]
    },
    
    skills: [
      { 
        categoria: "Testes & QA", 
        items: ["Testes Manuais", "Automação de Testes", "Testes de API", "Testes de Acessibilidade", "BDD", "Cucumber"] 
      },
      { 
        categoria: "Linguagens & Ferramentas", 
        items: ["Selenium", "Capybara", "Ruby", "JavaScript", "Jasmine", "TestLink"] 
      },
      { 
        categoria: "Metodologias", 
        items: ["CI/CD", "Quality Strategy", "Scrum", "Test Planning", "Agile"] 
      },
      { 
        categoria: "Soft Skills", 
        items: ["Docência", "Comunicação", "Liderança", "Análise Crítica", "Mentoria"] 
      }
    ],
    
    experiencia: [
      {
        titulo: "Professora Universitária",
        empresa: "Universidade de Marília",
        periodo: "agosto de 2025 - Presente",
        descricao: "Ministra a disciplina de Testes e Qualidade de Software com aulas teóricas e práticas sobre fundamentos de QA, automação, ciclo de vida do teste e ferramentas do mercado."
      },
      {
        titulo: "Analista de Testes III",
        empresa: "Tray",
        periodo: "junho de 2025 - Presente",
        descricao: "Manutenção de pipelines de Teste (CI/CD), análise de bugs, testes manuais e automatizados em plataforma de gestão de atendimentos."
      },
      {
        titulo: "Analista de Testes II",
        empresa: "Tray",
        periodo: "outubro de 2022 - junho de 2025",
        descricao: "Automação de testes em Ecommerce, participação em plannings e contribuição com qualidade do produto."
      }
    ],
    
    formacao: [
      {
        grau: "Pós-graduação Lato Sensu",
        curso: "Especialização em Segurança da Informação",
        instituicao: "Anhanguera Educacional",
        periodo: "agosto de 2025 - março de 2026"
      },
      {
        grau: "Pós-graduação Lato Sensu",
        curso: "MBA em Gestão Estratégica de Projetos e Metodologias",
        instituicao: "Descomplica",
        periodo: "dezembro de 2020 - novembro de 2021"
      },
      {
        grau: "Graduação",
        curso: "Análise e Desenvolvimento de Sistemas",
        instituicao: "Fatec Garça",
        periodo: "2017 - 2019"
      }
    ],
    
    certificacoes: [
      "Certified Tester Foundation Level (CTFL)",
      "Selenium: Testes automatizados de aceitação em .NET",
      "Automação de Testes com Capybara, Cucumber e Ruby",
      "Jasmine: Testes automatizados em JavaScript",
      "Cucumber e BDD para web apps"
    ]
  }

  return (
    <div className="portfolio-container">
      {/* HEADER */}
      <div className="portfolio-header">
        <div className="header-content">
          <div className="avatar">
            <div className="avatar-placeholder">
              👩‍💻
            </div>
          </div>
          
          <div className="header-info">
            <h1>{portfolioData.nome}</h1>
            <p className="titulo">{portfolioData.titulo}</p>
            <p className="locacao">📍 {portfolioData.locacao}</p>
            <p className="descricao">{portfolioData.descricao}</p>
            
            <div className="social-links">
              <a href={`mailto:${portfolioData.email}`} className="social-btn" title="Email">
                📧
              </a>
              <a href={`tel:${portfolioData.telefone}`} className="social-btn" title="Telefone">
                📱
              </a>
              <a href={portfolioData.linkedin} target="_blank" rel="noopener noreferrer" className="social-btn" title="LinkedIn">
                💼
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* TABS */}
      <div className="portfolio-tabs">
        <button 
          className={`tab-btn ${activeTab === 'sobre' ? 'active' : ''}`}
          onClick={() => setActiveTab('sobre')}
        >
          Sobre
        </button>
        <button 
          className={`tab-btn ${activeTab === 'skills' ? 'active' : ''}`}
          onClick={() => setActiveTab('skills')}
        >
          Habilidades
        </button>
        <button 
          className={`tab-btn ${activeTab === 'experiencia' ? 'active' : ''}`}
          onClick={() => setActiveTab('experiencia')}
        >
          Experiência
        </button>
        <button 
          className={`tab-btn ${activeTab === 'formacao' ? 'active' : ''}`}
          onClick={() => setActiveTab('formacao')}
        >
          Formação
        </button>
        <button 
          className={`tab-btn ${activeTab === 'certificacoes' ? 'active' : ''}`}
          onClick={() => setActiveTab('certificacoes')}
        >
          Certificações
        </button>
      </div>

      {/* CONTEÚDO */}
      <div className="portfolio-content">
        
        {/* SOBRE */}
        {activeTab === 'sobre' && (
          <div className="tab-content">
            <h2>Sobre Mim</h2>
            <p className="about-description">{portfolioData.sobre.descricao}</p>
            
            <h3>Destaques</h3>
            <ul className="highlights">
              {portfolioData.sobre.resumo.map((item, idx) => (
                <li key={idx}>{item}</li>
              ))}
            </ul>
          </div>
        )}

        {/* SKILLS */}
        {activeTab === 'skills' && (
          <div className="tab-content">
            <h2>Habilidades</h2>
            <div className="skills-grid">
              {portfolioData.skills.map((skillGroup, idx) => (
                <div key={idx} className="skill-group">
                  <h3>{skillGroup.categoria}</h3>
                  <div className="skill-items">
                    {skillGroup.items.map((skill, i) => (
                      <span key={i} className="skill-badge">{skill}</span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* EXPERIÊNCIA */}
        {activeTab === 'experiencia' && (
          <div className="tab-content">
            <h2>Experiência Profissional</h2>
            <div className="experience-list">
              {portfolioData.experiencia.map((exp, idx) => (
                <div key={idx} className="experience-item">
                  <div className="exp-header">
                    <h3>{exp.titulo}</h3>
                    <span className="periodo">{exp.periodo}</span>
                  </div>
                  <p className="empresa">🏢 {exp.empresa}</p>
                  <p className="descricao">{exp.descricao}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* FORMAÇÃO */}
        {activeTab === 'formacao' && (
          <div className="tab-content">
            <h2>Formação Acadêmica</h2>
            <div className="formacao-list">
              {portfolioData.formacao.map((form, idx) => (
                <div key={idx} className="formacao-item">
                  <div className="form-header">
                    <h3>{form.curso}</h3>
                    <span className="grau">{form.grau}</span>
                  </div>
                  <p className="instituicao">🎓 {form.instituicao}</p>
                  <p className="periodo-form">{form.periodo}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* CERTIFICAÇÕES */}
        {activeTab === 'certificacoes' && (
          <div className="tab-content">
            <h2>Certificações</h2>
            <div className="certificacoes-list">
              {portfolioData.certificacoes.map((cert, idx) => (
                <div key={idx} className="certificacao-item">
                  <span className="cert-badge">✅</span>
                  <span>{cert}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* CONTATO */}
      <div className="portfolio-footer">
        <h3>Vamos Conversar?</h3>
        <p>Estou aberta para Falar sobre QA, Testes e Educação em Tecnologia!</p>
        <div className="contact-info">
          <a href={`mailto:${portfolioData.email}`} className="contact-btn">
            📧 {portfolioData.email}
          </a>
          <a href={`tel:${portfolioData.telefone}`} className="contact-btn">
            📱 {portfolioData.telefone}
          </a>
          <a href={portfolioData.linkedin} target="_blank" rel="noopener noreferrer" className="contact-btn">
            💼 LinkedIn
          </a>
        </div>
      </div>
    </div>
  )
}