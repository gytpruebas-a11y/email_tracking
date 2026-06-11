import { useState } from "react";
import Aperturas from "./Aperturas";
import Importar from "./Importar";

function App() {
  const [pagina, setPagina] = useState("aperturas");

  return (
    <div>
      <div style={{ padding: "10px 20px", borderBottom: "1px solid #ccc" }}>
        <button
          onClick={() => setPagina("aperturas")}
          style={{ marginRight: "10px", fontWeight: pagina === "aperturas" ? "bold" : "normal" }}
        >
          📊 Aperturas
        </button>
        <button
          onClick={() => setPagina("importar")}
          style={{ fontWeight: pagina === "importar" ? "bold" : "normal" }}
        >
          📂 Importar Contactos
        </button>
      </div>
      {pagina === "aperturas" && <Aperturas />}
      {pagina === "importar" && <Importar />}
    </div>
  );
}

export default App;
