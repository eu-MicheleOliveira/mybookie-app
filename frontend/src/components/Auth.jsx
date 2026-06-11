import { useState } from 'react'
import { authService } from '../services/api'
import '../styles/Auth.css'

export default function Auth({ onLoginSuccess }) {
  const [isLogin, setIsLogin] = useState(true)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)

  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: ''
  })

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setSuccess(null)
    setLoading(true)

    try {
      if (isLogin) {
        const response = await authService.login(formData.email, formData.password)
        setSuccess('Login realizado com sucesso!')
        onLoginSuccess(response.data)
      } else {
        await authService.register(formData.email, formData.username, formData.password)
        setSuccess('Conta criada com sucesso! Faça login.')
        setIsLogin(true)
        setFormData({ email: '', username: '', password: '' })
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro na operação')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div id="auth-container" data-testid="auth-container" className="auth-container">
      <div id="auth-card" data-testid="auth-card" className="auth-card">
        <h1 id="auth-title" data-testid="auth-title">📚 Mybookie</h1>
        <p id="auth-subtitle" data-testid="auth-subtitle">{isLogin ? 'Bem-vinda de volta!' : 'Crie sua conta'}</p>

        {error && (
          <div id="auth-error" data-testid="auth-error" className="alert alert-error">
            ❌ {error}
          </div>
        )}
        {success && (
          <div id="auth-success" data-testid="auth-success" className="alert alert-success">
            ✅ {success}
          </div>
        )}

        <form id="auth-form" data-testid="auth-form" onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="auth-email-input">Email *</label>
            <input
              id="auth-email-input"
              data-testid="auth-email-input"
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              placeholder="seu@email.com"
            />
          </div>

          {!isLogin && (
            <div className="form-group">
              <label htmlFor="auth-username-input">Usuário *</label>
              <input
                id="auth-username-input"
                data-testid="auth-username-input"
                type="text"
                name="username"
                value={formData.username}
                onChange={handleChange}
                required
                placeholder="seu_usuario"
              />
            </div>
          )}

          <div className="form-group">
            <label htmlFor="auth-password-input">Senha *</label>
            <input
              id="auth-password-input"
              data-testid="auth-password-input"
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="••••••••"
            />
          </div>

          <button 
            id="auth-submit-btn"
            data-testid="auth-submit-btn"
            type="submit" 
            disabled={loading}
            className="btn-submit"
          >
            {loading ? '⏳ Aguarde...' : (isLogin ? '🔓 Entrar' : '✍️ Registrar')}
          </button>
        </form>

        <div className="auth-toggle">
          <p id="auth-toggle-text" data-testid="auth-toggle-text">
            {isLogin ? 'Não tem conta? ' : 'Já tem conta? '}
            <button
              id="auth-toggle-btn"
              data-testid="auth-toggle-btn"
              type="button"
              onClick={() => setIsLogin(!isLogin)}
              className="toggle-btn"
            >
              {isLogin ? 'Registre-se' : 'Faça login'}
            </button>
          </p>
        </div>
      </div>
    </div>
  )
}