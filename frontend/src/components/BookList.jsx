import { useState, useEffect } from "react";
import { booksService } from "../services/api";
import ConfirmModal from "./ConfirmModal";
import "../styles/BookList.css";

const CATEGORIAS = [
  { value: "Ficção", label: "Ficção" },
  { value: "Romance", label: "Romance" },
  { value: "Fantasia", label: "Fantasia" },
  { value: "Tecnologia", label: "Tecnologia" },
  { value: "História", label: "História" },
  { value: "Educação", label: "Educação" },
  { value: "Ciência", label: "Ciência" },
  { value: "Infantil", label: "Infantil" },
  { value: "Poesia", label: "Poesia" },
  { value: "Biografia", label: "Biografia" },
  { value: "Autoajuda", label: "Autoajuda" },
  { value: "Negócios", label: "Negócios" },
];

export default function BookList() {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [deleteBookId, setDeleteBookId] = useState(null);

  const [filterNome, setFilterNome] = useState("");
  const [filterLido, setFilterLido] = useState("todos");

  const [formData, setFormData] = useState({
    titulo: "",
    autor: "",
    categoria: "Ficção",
    lido: false,
    avaliacao: 0,
  });

  useEffect(() => {
    loadBooks();
  }, []);

  const loadBooks = async () => {
    try {
      setLoading(true);
      const response = await booksService.listBooks();
      setBooks(response.data || response);
    } catch (err) {
      setError("Erro ao carregar livros");
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleStarClick = (star) => {
    setFormData((prev) => ({
      ...prev,
      avaliacao: star,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    try {
      if (editingId) {
        await booksService.updateBook(editingId, formData);
        setSuccess("Livro atualizado com sucesso!");
      } else {
        await booksService.createBook(formData);
        setSuccess("Livro criado com sucesso!");
      }

      setFormData({
        titulo: "",
        autor: "",
        categoria: "Ficção",
        lido: false,
        avaliacao: 0,
      });
      setShowForm(false);
      setEditingId(null);
      loadBooks();
    } catch (err) {
      setError(err.response?.data?.detail || "Erro ao salvar livro");
    }
  };

  const handleEdit = (book) => {
    setFormData(book);
    setEditingId(book.id);
    setShowForm(true);
  };

  const handleDelete = (id) => {
    setDeleteBookId(id);
    setConfirmDelete(true);
  };

  const confirmDeleteBook = async () => {
    if (!deleteBookId) return;

    try {
      await booksService.deleteBook(deleteBookId);
      setSuccess("Livro deletado com sucesso!");
      setConfirmDelete(false);
      setDeleteBookId(null);
      loadBooks();
    } catch (err) {
      setError("Erro ao deletar livro");
      setConfirmDelete(false);
    }
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingId(null);
    setFormData({
      titulo: "",
      autor: "",
      categoria: "Ficção",
      lido: false,
      avaliacao: 0,
    });
  };

  const booksFiltrados = books.filter((book) => {
    const matchNome =
      filterNome === "" ||
      book.titulo.toLowerCase().includes(filterNome.toLowerCase());
    const matchLido =
      filterLido === "todos" ||
      (filterLido === "lido" && book.lido === true) ||
      (filterLido === "nao-lido" && book.lido === false);
    return matchNome && matchLido;
  });

  const renderStars = (avaliacao, isEditable = false, callback = null) => {
    return (
      <div className="stars-container-wrapper">
        <div
          id="stars-rating"
          data-testid="stars-rating"
          className="stars-rating"
        >
          {[1, 2, 3, 4, 5].map((star) => (
            <span
              key={star}
              id={`star-${star}`}
              data-testid={`star-${star}`}
              className={`star ${star <= avaliacao ? "filled" : ""} ${isEditable ? "editable" : ""}`}
              onClick={() => isEditable && callback && callback(star)}
              style={{ cursor: isEditable ? "pointer" : "default" }}
            >
              ★
            </span>
          ))}
        </div>
        {avaliacao > 0 && <span className="stars-text">{avaliacao}/5</span>}
      </div>
    );
  };

  if (loading)
    return (
      <div
        id="loading-container"
        data-testid="loading-container"
        className="container"
      >
        <p>⏳ Carregando livros...</p>
      </div>
    );

  return (
    <>
      <ConfirmModal
        isOpen={confirmDelete}
        title="🗑️ Deletar Livro"
        message="Tem certeza que deseja deletar este livro? Esta ação não pode ser desfeita."
        confirmText="Sim, Deletar"
        cancelText="Cancelar"
        isDanger={true}
        onConfirm={confirmDeleteBook}
        onCancel={() => {
          setConfirmDelete(false);
          setDeleteBookId(null);
        }}
      />

      <div
        id="book-list-container"
        data-testid="book-list-container"
        className="container book-list-container"
      >
        <div id="book-header" data-testid="book-header" className="book-header">
          <h1 id="book-title" data-testid="book-title">
            📚 Minha Biblioteca
          </h1>
          <button
            id="btn-toggle-form"
            data-testid="btn-toggle-form"
            className="btn-add"
            onClick={() => setShowForm(!showForm)}
          >
            {showForm ? "✕ Fechar" : "➕ Novo Livro"}
          </button>
        </div>

        {error && (
          <div
            id="book-error-alert"
            data-testid="book-error-alert"
            className="alert alert-error"
          >
            ❌ {error}
          </div>
        )}
        {success && (
          <div
            id="book-success-alert"
            data-testid="book-success-alert"
            className="alert alert-success"
          >
            ✅ {success}
          </div>
        )}

        {showForm && (
          <div
            id="book-form-container"
            data-testid="book-form-container"
            className="form-container"
          >
            <h2 id="form-title" data-testid="form-title">
              {editingId ? "✏️ Editar Livro" : "➕ Novo Livro"}
            </h2>
            <form
              id="book-form"
              data-testid="book-form"
              onSubmit={handleSubmit}
              className="book-form"
            >
              <div className="form-group">
                <label htmlFor="input-titulo">Título *</label>
                <input
                  id="input-titulo"
                  data-testid="input-titulo"
                  type="text"
                  name="titulo"
                  value={formData.titulo}
                  onChange={handleChange}
                  required
                  placeholder="Digite o título"
                />
              </div>

              <div className="form-group">
                <label htmlFor="input-autor">Autor *</label>
                <input
                  id="input-autor"
                  data-testid="input-autor"
                  type="text"
                  name="autor"
                  value={formData.autor}
                  onChange={handleChange}
                  required
                  placeholder="Digite o autor"
                />
              </div>

              <div className="form-group">
                <label htmlFor="select-categoria">Categoria *</label>
                <select
                  id="select-categoria"
                  data-testid="select-categoria"
                  name="categoria"
                  value={formData.categoria}
                  onChange={handleChange}
                  required
                >
                  {CATEGORIAS.map((cat) => (
                    <option key={cat.value} value={cat.value}>
                      {cat.label}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="select-lido">Já leu? *</label>
                <select
                  id="select-lido"
                  data-testid="select-lido"
                  name="lido"
                  value={formData.lido ? "sim" : "nao"}
                  onChange={(e) =>
                    setFormData((prev) => ({
                      ...prev,
                      lido: e.target.value === "sim",
                      avaliacao: e.target.value === "nao" ? 0 : prev.avaliacao,
                    }))
                  }
                  required
                >
                  <option value="nao">Ainda não li</option>
                  <option value="sim">Já li</option>
                </select>
              </div>

              {formData.lido && (
                <div
                  id="avaliacao-container"
                  data-testid="avaliacao-container"
                  className="form-group stars-container"
                >
                  <label>Avaliação</label>
                  {renderStars(formData.avaliacao, true, handleStarClick)}
                </div>
              )}

              <div
                id="form-buttons"
                data-testid="form-buttons"
                className="form-buttons"
              >
                <button
                  id="btn-submit-form"
                  data-testid="btn-submit-form"
                  type="submit"
                  className="btn-submit"
                >
                  {editingId ? "💾 Atualizar" : "➕ Adicionar"}
                </button>
                <button
                  id="btn-cancel-form"
                  data-testid="btn-cancel-form"
                  type="button"
                  className="btn-cancel"
                  onClick={handleCancel}
                >
                  ✕ Cancelar
                </button>
              </div>
            </form>
          </div>
        )}

        {!showForm && booksFiltrados.length > 0 && (
          <div
            id="filters-container"
            data-testid="filters-container"
            className="filters-container"
          >
            <input
              id="filter-nome"
              data-testid="filter-nome"
              type="text"
              placeholder="🔍 Pesquisar por nome..."
              value={filterNome}
              onChange={(e) => setFilterNome(e.target.value)}
              className="filter-input"
            />

            <select
              id="filter-lido"
              data-testid="filter-lido"
              value={filterLido}
              onChange={(e) => setFilterLido(e.target.value)}
              className="filter-select"
            >
              <option value="todos">Todos os livros</option>
              <option value="lido">Já li</option>
              <option value="nao-lido">Ainda não li</option>
            </select>
          </div>
        )}

        {!showForm && booksFiltrados.length === 0 ? (
          <div
            id="empty-state"
            data-testid="empty-state"
            className="empty-state"
          >
            <p>📭 Nenhum livro encontrado</p>
            {filterNome || filterLido !== "todos" ? (
              <p>Tente ajustar seus filtros</p>
            ) : (
              <p>Clique em "Novo Livro" para começar!</p>
            )}
          </div>
        ) : (
          !showForm && (
            <div
              id="books-grid"
              data-testid="books-grid"
              className="books-grid"
            >
              {booksFiltrados.map((book) => (
                <div
                  key={book.id}
                  id={`book-card-${book.id}`}
                  data-testid={`book-card-${book.id}`}
                  className="book-card"
                >
                  <div className="book-card-header">
                    <h3
                      id={`book-titulo-${book.id}`}
                      data-testid={`book-titulo-${book.id}`}
                    >
                      {book.titulo}
                    </h3>
                    <span
                      id={`book-categoria-${book.id}`}
                      data-testid={`book-categoria-${book.id}`}
                      className="category-badge"
                    >
                      {book.categoria}
                    </span>
                  </div>

                  <div className="book-card-body">
                    <p>
                      <strong>Autor:</strong>
                      <span
                        id={`book-autor-${book.id}`}
                        data-testid={`book-autor-${book.id}`}
                      >
                        {book.autor}
                      </span>
                    </p>

                    <p
                      id={`book-status-${book.id}`}
                      data-testid={`book-status-${book.id}`}
                      className="status-lido"
                    >
                      {book.lido ? "✅ Já li" : "📖 Ainda não li"}
                    </p>

                    {book.lido && book.avaliacao > 0 && (
                      <div
                        id={`book-avaliacao-${book.id}`}
                        data-testid={`book-avaliacao-${book.id}`}
                        className="avaliacao"
                      >
                        <strong>Avaliação:</strong>
                        {renderStars(book.avaliacao)}
                      </div>
                    )}
                  </div>

                  <div className="book-card-actions">
                    <button
                      id={`btn-edit-${book.id}`}
                      data-testid={`btn-edit-${book.id}`}
                      className="btn-edit"
                      onClick={() => handleEdit(book)}
                    >
                      ✏️ Editar
                    </button>
                    <button
                      id={`btn-delete-${book.id}`}
                      data-testid={`btn-delete-${book.id}`}
                      className="btn-delete"
                      onClick={() => handleDelete(book.id)}
                    >
                      🗑️ Deletar
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )
        )}
      </div>
    </>
  );
}
