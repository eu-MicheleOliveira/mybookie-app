import '../styles/ConfirmModal.css'

export default function ConfirmModal({ isOpen, title, message, onConfirm, onCancel, confirmText = "Confirmar", cancelText = "Cancelar", isDanger = false }) {
  if (!isOpen) return null

  return (
    <div id="modal-overlay" data-testid="modal-overlay" className="modal-overlay">
      <div id="modal-box" data-testid="modal-box" className="modal-box">
        <h3 id="modal-title" data-testid="modal-title">{title}</h3>
        <p id="modal-message" data-testid="modal-message">{message}</p>
        
        <div id="modal-buttons" data-testid="modal-buttons" className="modal-buttons">
          <button 
            id="modal-btn-confirm"
            data-testid="modal-btn-confirm"
            className={`modal-btn ${isDanger ? 'danger' : 'primary'}`}
            onClick={onConfirm}
          >
            {confirmText}
          </button>
          <button 
            id="modal-btn-cancel"
            data-testid="modal-btn-cancel"
            className="modal-btn secondary"
            onClick={onCancel}
          >
            {cancelText}
          </button>
        </div>
      </div>
    </div>
  )
}