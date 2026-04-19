export default function ScenarioSelector({ scenarios, selectedIndex, onSelect }) {
  return (
    <div style={{ marginBottom: 20 }}>
      <label>Scenario: </label>
      <select
        value={selectedIndex}
        onChange={(e) => onSelect(Number(e.target.value))}
      >
        {scenarios.map((s, i) => (
          <option key={i} value={i}>
            {s.name}
          </option>
        ))}
      </select>
    </div>
  );
}