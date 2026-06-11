import { useState } from "react";

function Importar() {
  const [token, setToken] = useState("");
  const [file, setFile] = useState(null);
  const [resultado, setResultado] = useState(null);
  const [error, setError] = useState(null);
  const [cargando, setCargando] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !token) return;

    setCargando(true);
    setResultado(null);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`/api/importar?token=${encodeURIComponent(token)}`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.detail || "Error al importar");
      } else {
        setResultado(data);
      }
    } catch (err) {
      setError("No se pudo conectar con el servidor");
    } finally {
      setCargando(false);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>📂 Importar Contactos</h2>
      <form onSubmit={handleSubmit}>
        <table border="1" cellPadding="8">
          <tbody>
            <tr>
              <td><strong>Token</strong></td>
              <td>
                <input
                  type="password"
                  value={token}
                  onChange={(e) => setToken(e.target.value)}
                  placeholder="Token de seguridad"
                  required
                />
              </td>
            </tr>
            <tr>
              <td><strong>Archivo CSV</strong></td>
              <td>
                <input
                  type="file"
                  accept=".csv"
                  onChange={(e) => setFile(e.target.files[0])}
                  required
                />
              </td>
            </tr>
            <tr>
              <td colSpan="2">
                <button type="submit" disabled={cargando}>
                  {cargando ? "Importando..." : "Importar"}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </form>

      {error && (
        <p style={{ color: "red", marginTop: "12px" }}>❌ {error}</p>
      )}

      {resultado && (
        <div style={{ marginTop: "12px" }}>
          <table border="1" cellPadding="8">
            <thead>
              <tr>
                <th>Insertados</th>
                <th>Omitidos</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{resultado.insertados}</td>
                <td>{resultado.omitidos}</td>
              </tr>
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Importar;
