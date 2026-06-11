import { useEffect, useState } from "react";

function Aperturas() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8002/api/aperturas")
      .then(res => res.json())
      .then(setData);
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h2>📊 Conteo de Aperturas</h2>
      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>Correo</th>
            <th>Total Aperturas</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, i) => (
            <tr key={i}>
              <td>{item.correo}</td>
              <td>{item.total_aperturas}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Aperturas;
