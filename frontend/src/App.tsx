import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Layout } from './Layout'
import { Teams } from './pages/Teams'
import { TeamDetail } from './pages/TeamDetail'
import { Players } from './pages/Players'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/teams" replace />} />
          <Route path="teams" element={<Teams />} />
          <Route path="teams/:teamId" element={<TeamDetail />} />
          <Route path="players" element={<Players />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
