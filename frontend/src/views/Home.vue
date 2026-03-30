<template>
  <div class="home-container">
    <!-- Announcement bar: Spanish adaptation by Manuel Peña - EnPixeles Lab -->
    <div class="announcement-bar">
      <span class="announcement-text">Adaptado al español para el mercado hispano por <strong>Manuel Peña</strong> — EnPíxeles Lab</span>
      <div class="announcement-links">
        <a href="https://www.instagram.com/enpixelesmedia/" target="_blank" rel="noopener" class="announcement-link" title="Instagram">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
            <circle cx="12" cy="12" r="4"></circle>
            <circle cx="17.5" cy="6.5" r="0.5" fill="currentColor" stroke="none"></circle>
          </svg>
        </a>
        <a href="https://www.youtube.com/@enpixelamedia" target="_blank" rel="noopener" class="announcement-link" title="YouTube">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22.54 6.42a2.78 2.78 0 0 0-1.95-1.96C18.88 4 12 4 12 4s-6.88 0-8.59.46A2.78 2.78 0 0 0 1.46 6.42 29 29 0 0 0 1 12a29 29 0 0 0 .46 5.58 2.78 2.78 0 0 0 1.95 1.96C5.12 20 12 20 12 20s6.88 0 8.59-.46a2.78 2.78 0 0 0 1.95-1.96A29 29 0 0 0 23 12a29 29 0 0 0-.46-5.58z"></path>
            <polygon points="9.75 15.02 15.5 12 9.75 8.98 9.75 15.02" fill="currentColor" stroke="none"></polygon>
          </svg>
        </a>
        <a href="https://www.linkedin.com/in/expixeles/" target="_blank" rel="noopener" class="announcement-link" title="LinkedIn">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path>
            <rect x="2" y="9" width="4" height="12"></rect>
            <circle cx="4" cy="4" r="2"></circle>
          </svg>
        </a>
        <a href="https://x.com/Enpixelesmedia" target="_blank" rel="noopener" class="announcement-link" title="X / Twitter">
          <svg viewBox="0 0 24 24" width="13" height="13" fill="currentColor">
            <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.748l7.73-8.835L1.254 2.25H8.08l4.259 5.631 5.905-5.631zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
          </svg>
        </a>
      </div>
    </div>

    <!-- Barra de navegación superior -->
    <nav class="navbar">
      <div class="nav-brand">MIROFISH</div>
      <div class="nav-links">
        <a href="https://github.com/666ghj/MiroFish" target="_blank" class="github-link">
          Visitar nuestra página de Github <span class="arrow">↗</span>
        </a>
      </div>
    </nav>

    <div class="main-content">
      <!-- Parte superior: Área Hero -->
      <section class="hero-section">
        <div class="hero-left">
          <div class="tag-row">
            <span class="orange-tag">Motor de inteligencia colectiva simple y universal</span>
            <span class="version-text">/ v0.1-Vista previa</span>
          </div>
          
          <h1 class="main-title">
            Sube cualquier informe<br>
            <span class="gradient-text">Predice el futuro al instante</span>
          </h1>
          
          <div class="hero-desc">
            <p>
              Incluso con solo un párrafo de texto, <span class="highlight-bold">MiroFish</span> puede generar automáticamente un mundo paralelo compuesto por hasta <span class="highlight-orange">millones de Agentes</span>. Inyecta variables desde una perspectiva global y busca la <span class="highlight-code">"solución local óptima"</span>
            </p>
            <p class="slogan-text">
              Que el futuro se ensaye entre Agentes, que las decisiones triunfen tras mil batallas<span class="blinking-cursor">_</span>
            </p>
          </div>
           
          <div class="decoration-square"></div>
        </div>
        
        <div class="hero-right">
          <!-- Área del Logo -->
          <div class="logo-container">
            <img src="../assets/logo/MiroFish_logo_left.jpeg" alt="MiroFish Logo" class="hero-logo" />
          </div>
          
          <button class="scroll-down-btn" @click="scrollToBottom">
            ↓
          </button>
        </div>
      </section>

      <!-- Parte inferior: Diseño de dos columnas -->
      <section class="dashboard-section">
        <!-- Columna izquierda: Estado y pasos -->
        <div class="left-panel">
          <div class="panel-header">
            <span class="status-dot">■</span> Estado del sistema
          </div>
          
          <h2 class="section-title">Listo</h2>
          <p class="section-desc">
            Motor de predicción en espera. Sube múltiples archivos no estructurados para inicializar la secuencia de simulación
          </p>
          
          <!-- Tarjetas de métricas -->
          <div class="metrics-row">
            <div class="metric-card">
              <div class="metric-value">Bajo costo</div>
              <div class="metric-label">Simulación estándar: promedio $5/vez</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">Alta disponibilidad</div>
              <div class="metric-label">Hasta millones de Agentes en simulación</div>
            </div>
          </div>

          <!-- Descripción de pasos de simulación (nueva sección) -->
          <div class="steps-container">
            <div class="steps-header">
               <span class="diamond-icon">◇</span> Secuencia de flujo de trabajo
            </div>
            <div class="workflow-list">
              <div class="workflow-item">
                <span class="step-num">01</span>
                <div class="step-info">
                  <div class="step-title">Construcción del grafo</div>
                  <div class="step-desc">Extracción de semillas reales & inyección de memoria individual y grupal & construcción GraphRAG</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">02</span>
                <div class="step-info">
                  <div class="step-title">Configuración del entorno</div>
                  <div class="step-desc">Extracción de relaciones de entidades & generación de perfiles & inyección de parámetros de simulación en Agent</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">03</span>
                <div class="step-info">
                  <div class="step-title">Iniciar simulación</div>
                  <div class="step-desc">Simulación paralela en dos plataformas & análisis automático de requisitos de predicción & actualización dinámica de memoria temporal</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">04</span>
                <div class="step-info">
                  <div class="step-title">Generación de informe</div>
                  <div class="step-desc">ReportAgent tiene un rico conjunto de herramientas para interactuar profundamente con el entorno post-simulación</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">05</span>
                <div class="step-info">
                  <div class="step-title">Interacción profunda</div>
                  <div class="step-desc">Conversa con cualquier participante del mundo simulado & con ReportAgent</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Columna derecha: Consola de interacción -->
        <div class="right-panel">
          <div class="console-box">
            <!-- Área de carga -->
            <div class="console-section">
              <div class="console-header">
                <span class="console-label">01 / Semilla real</span>
                <span class="console-meta">Formatos soportados: PDF, MD, TXT</span>
              </div>
              
              <div 
                class="upload-zone"
                :class="{ 'drag-over': isDragOver, 'has-files': files.length > 0 }"
                @dragover.prevent="handleDragOver"
                @dragleave.prevent="handleDragLeave"
                @drop.prevent="handleDrop"
                @click="triggerFileInput"
              >
                <input
                  ref="fileInput"
                  type="file"
                  multiple
                  accept=".pdf,.md,.txt"
                  @change="handleFileSelect"
                  style="display: none"
                  :disabled="loading"
                />
                
                <div v-if="files.length === 0" class="upload-placeholder">
                  <div class="upload-icon">↑</div>
                  <div class="upload-title">Arrastra archivos para subir</div>
                  <div class="upload-hint">O haz clic para explorar el sistema de archivos</div>
                </div>
                
                <div v-else class="file-list">
                  <div v-for="(file, index) in files" :key="index" class="file-item">
                    <span class="file-icon">📄</span>
                    <span class="file-name">{{ file.name }}</span>
                    <button @click.stop="removeFile(index)" class="remove-btn">×</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Separador -->
            <div class="console-divider">
              <span>Ingresar parámetros</span>
            </div>

            <!-- Área de entrada -->
            <div class="console-section">
              <div class="console-header">
                <span class="console-label">>_ 02 / Prompt de simulación</span>
              </div>
              <div class="input-wrapper">
                <textarea
                  v-model="formData.simulationRequirement"
                  class="code-input"
                  placeholder="// Ingresa en lenguaje natural el requisito de simulación (ej. ¿Qué opinión pública generaría si la universidad revocara la sanción de cierto estudiante?)"
                  rows="6"
                  :disabled="loading"
                ></textarea>
                <div class="model-badge">Motor: MiroFish-V1.0</div>
              </div>
            </div>

            <!-- Botón de inicio -->
            <div class="console-section btn-section">
              <button 
                class="start-engine-btn"
                @click="startSimulation"
                :disabled="!canSubmit || loading"
              >
                <span v-if="!loading">Iniciar motor</span>
                <span v-else>Inicializando...</span>
                <span class="btn-arrow">→</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Base de datos de proyectos históricos -->
      <HistoryDatabase />

      <!-- Spanish adaptation by Manuel Peña - EnPixeles Lab - Based on MiroFish by 666ghj AGPL-3.0 -->
      <footer class="credits-footer">
        <span class="credits-text">Adaptado al español para el mercado hispano por <strong>Manuel Peña</strong> — EnPíxeles Lab</span>
        <div class="credits-links">
          <!-- Instagram -->
          <a href="https://www.instagram.com/enpixelesmedia/" target="_blank" rel="noopener" class="credits-link" title="Instagram">
            <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
              <circle cx="12" cy="12" r="4"></circle>
              <circle cx="17.5" cy="6.5" r="0.5" fill="currentColor" stroke="none"></circle>
            </svg>
          </a>
          <!-- YouTube -->
          <a href="https://www.youtube.com/@enpixelamedia" target="_blank" rel="noopener" class="credits-link" title="YouTube">
            <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22.54 6.42a2.78 2.78 0 0 0-1.95-1.96C18.88 4 12 4 12 4s-6.88 0-8.59.46A2.78 2.78 0 0 0 1.46 6.42 29 29 0 0 0 1 12a29 29 0 0 0 .46 5.58 2.78 2.78 0 0 0 1.95 1.96C5.12 20 12 20 12 20s6.88 0 8.59-.46a2.78 2.78 0 0 0 1.95-1.96A29 29 0 0 0 23 12a29 29 0 0 0-.46-5.58z"></path>
              <polygon points="9.75 15.02 15.5 12 9.75 8.98 9.75 15.02" fill="currentColor" stroke="none"></polygon>
            </svg>
          </a>
          <!-- LinkedIn -->
          <a href="https://www.linkedin.com/in/expixeles/" target="_blank" rel="noopener" class="credits-link" title="LinkedIn">
            <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path>
              <rect x="2" y="9" width="4" height="12"></rect>
              <circle cx="4" cy="4" r="2"></circle>
            </svg>
          </a>
          <!-- X/Twitter -->
          <a href="https://x.com/Enpixelesmedia" target="_blank" rel="noopener" class="credits-link" title="X / Twitter">
            <svg viewBox="0 0 24 24" width="15" height="15" fill="currentColor">
              <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.748l7.73-8.835L1.254 2.25H8.08l4.259 5.631 5.905-5.631zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
            </svg>
          </a>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import HistoryDatabase from '../components/HistoryDatabase.vue'

const router = useRouter()

// Datos del formulario
const formData = ref({
  simulationRequirement: ''
})

// Lista de archivos
const files = ref([])

// Estado
const loading = ref(false)
const error = ref('')
const isDragOver = ref(false)

// Referencia al input de archivos
const fileInput = ref(null)

// Propiedad computada: si se puede enviar
const canSubmit = computed(() => {
  return formData.value.simulationRequirement.trim() !== '' && files.value.length > 0
})

// Activar selección de archivos
const triggerFileInput = () => {
  if (!loading.value) {
    fileInput.value?.click()
  }
}

// Manejar selección de archivos
const handleFileSelect = (event) => {
  const selectedFiles = Array.from(event.target.files)
  addFiles(selectedFiles)
}

// Manejar eventos de arrastrar y soltar
const handleDragOver = (e) => {
  if (!loading.value) {
    isDragOver.value = true
  }
}

const handleDragLeave = (e) => {
  isDragOver.value = false
}

const handleDrop = (e) => {
  isDragOver.value = false
  if (loading.value) return
  
  const droppedFiles = Array.from(e.dataTransfer.files)
  addFiles(droppedFiles)
}

// Agregar archivos
const addFiles = (newFiles) => {
  const validFiles = newFiles.filter(file => {
    const ext = file.name.split('.').pop().toLowerCase()
    return ['pdf', 'md', 'txt'].includes(ext)
  })
  files.value.push(...validFiles)
}

// Eliminar archivos
const removeFile = (index) => {
  files.value.splice(index, 1)
}

// Desplazarse hacia abajo
const scrollToBottom = () => {
  window.scrollTo({
    top: document.body.scrollHeight,
    behavior: 'smooth'
  })
}

// Iniciar simulación - redirigir inmediatamente, llamada API en la página Process
const startSimulation = () => {
  if (!canSubmit.value || loading.value) return
  
  // Almacenar los datos pendientes de subida
  import('../store/pendingUpload.js').then(({ setPendingUpload }) => {
    setPendingUpload(files.value, formData.value.simulationRequirement)
    
    // Redirigir a la página Process (identificador especial para proyecto nuevo)
    router.push({
      name: 'Process',
      params: { projectId: 'new' }
    })
  })
}
</script>

<style scoped>
/* Variables globales y reset */
:root {
  --black: #000000;
  --white: #FFFFFF;
  --orange: #FF4500;
  --gray-light: #F5F5F5;
  --gray-text: #666666;
  --border: #E5E5E5;
  /* 
    Usar Space Grotesk como fuente de títulos, JetBrains Mono como fuente de código/etiquetas
    Asegurarse de importar estas Google Fonts en index.html 
  */
  --font-mono: 'JetBrains Mono', monospace;
  --font-sans: 'Space Grotesk', 'Noto Sans SC', system-ui, sans-serif;
  --font-cn: 'Noto Sans SC', system-ui, sans-serif;
}

.home-container {
  min-height: 100vh;
  background: var(--white);
  font-family: var(--font-sans);
  color: var(--black);
}

/* Announcement bar */
.announcement-bar {
  background: #0A0A0A;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  padding: 9px 40px;
  position: relative;
}

.announcement-text {
  font-family: var(--font-sans);
  font-size: 0.78rem;
  font-weight: 400;
  letter-spacing: 0.2px;
  color: #C8C8C8;
}

.announcement-text strong {
  color: #FFFFFF;
  font-weight: 600;
}

.announcement-links {
  display: flex;
  align-items: center;
  gap: 14px;
}

.announcement-link {
  color: #666;
  display: flex;
  align-items: center;
  text-decoration: none;
  transition: color 0.2s ease;
}

.announcement-link:hover {
  color: #FFFFFF;
}

/* Navegación superior */
.navbar {
  height: 60px;
  background: var(--black);
  color: var(--white);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
}

.nav-brand {
  font-family: var(--font-mono);
  font-weight: 800;
  letter-spacing: 1px;
  font-size: 1.2rem;
}

.nav-links {
  display: flex;
  align-items: center;
}

.github-link {
  color: var(--white);
  text-decoration: none;
  font-family: var(--font-mono);
  font-size: 0.9rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: opacity 0.2s;
}

.github-link:hover {
  opacity: 0.8;
}

.arrow {
  font-family: sans-serif;
}

/* Área de contenido principal */
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 60px 40px;
}

/* Área Hero */
.hero-section {
  display: flex;
  justify-content: space-between;
  margin-bottom: 80px;
  position: relative;
}

.hero-left {
  flex: 1;
  padding-right: 60px;
}

.tag-row {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
  font-family: var(--font-mono);
  font-size: 0.8rem;
}

.orange-tag {
  background: var(--orange);
  color: var(--white);
  padding: 4px 10px;
  font-weight: 700;
  letter-spacing: 1px;
  font-size: 0.75rem;
}

.version-text {
  color: #999;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.main-title {
  font-size: 4.5rem;
  line-height: 1.2;
  font-weight: 500;
  margin: 0 0 40px 0;
  letter-spacing: -2px;
  color: var(--black);
}

.gradient-text {
  background: linear-gradient(90deg, #000000 0%, #444444 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
}

.hero-desc {
  font-size: 1.05rem;
  line-height: 1.8;
  color: var(--gray-text);
  max-width: 640px;
  margin-bottom: 50px;
  font-weight: 400;
  text-align: justify;
}

.hero-desc p {
  margin-bottom: 1.5rem;
}

.highlight-bold {
  color: var(--black);
  font-weight: 700;
}

.highlight-orange {
  color: var(--orange);
  font-weight: 700;
  font-family: var(--font-mono);
}

.highlight-code {
  background: rgba(0, 0, 0, 0.05);
  padding: 2px 6px;
  border-radius: 2px;
  font-family: var(--font-mono);
  font-size: 0.9em;
  color: var(--black);
  font-weight: 600;
}

.slogan-text {
  font-size: 1.2rem;
  font-weight: 520;
  color: var(--black);
  letter-spacing: 1px;
  border-left: 3px solid var(--orange);
  padding-left: 15px;
  margin-top: 20px;
}

.blinking-cursor {
  color: var(--orange);
  animation: blink 1s step-end infinite;
  font-weight: 700;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.decoration-square {
  width: 16px;
  height: 16px;
  background: var(--orange);
}

.hero-right {
  flex: 0.8;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-end;
}

.logo-container {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  padding-right: 40px;
}

.hero-logo {
  max-width: 500px; /* Ajustar tamaño del logo */
  width: 100%;
}

.scroll-down-btn {
  width: 40px;
  height: 40px;
  border: 1px solid var(--border);
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--orange);
  font-size: 1.2rem;
  transition: all 0.2s;
}

.scroll-down-btn:hover {
  border-color: var(--orange);
}

/* Diseño de dos columnas del Dashboard */
.dashboard-section {
  display: flex;
  gap: 60px;
  border-top: 1px solid var(--border);
  padding-top: 60px;
  align-items: flex-start;
}

.dashboard-section .left-panel,
.dashboard-section .right-panel {
  display: flex;
  flex-direction: column;
}

/* Panel izquierdo */
.left-panel {
  flex: 0.8;
}

.panel-header {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: #999;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
}

.status-dot {
  color: var(--orange);
  font-size: 0.8rem;
}

.section-title {
  font-size: 2rem;
  font-weight: 520;
  margin: 0 0 15px 0;
}

.section-desc {
  color: var(--gray-text);
  margin-bottom: 25px;
  line-height: 1.6;
}

.metrics-row {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}

.metric-card {
  border: 1px solid var(--border);
  padding: 20px 30px;
  min-width: 150px;
}

.metric-value {
  font-family: var(--font-mono);
  font-size: 1.8rem;
  font-weight: 520;
  margin-bottom: 5px;
}

.metric-label {
  font-size: 0.85rem;
  color: #999;
}

/* Descripción de pasos de simulación */
.steps-container {
  border: 1px solid var(--border);
  padding: 30px;
  position: relative;
}

.steps-header {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: #999;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.diamond-icon {
  font-size: 1.2rem;
  line-height: 1;
}

.workflow-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.workflow-item {
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

.step-num {
  font-family: var(--font-mono);
  font-weight: 700;
  color: var(--black);
  opacity: 0.3;
}

.step-info {
  flex: 1;
}

.step-title {
  font-weight: 520;
  font-size: 1rem;
  margin-bottom: 4px;
}

.step-desc {
  font-size: 0.85rem;
  color: var(--gray-text);
}

/* Consola de interacción derecha */
.right-panel {
  flex: 1.2;
}

.console-box {
  border: 1px solid #CCC; /* Borde externo sólido */
  padding: 8px; /* Relleno que crea sensación de doble borde */
}

.console-section {
  padding: 20px;
}

.console-section.btn-section {
  padding-top: 0;
}

.console-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: #666;
}

.upload-zone {
  border: 1px dashed #CCC;
  height: 200px;
  overflow-y: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  background: #FAFAFA;
}

.upload-zone.has-files {
  align-items: flex-start;
}

.upload-zone:hover {
  background: #F0F0F0;
  border-color: #999;
}

.upload-placeholder {
  text-align: center;
}

.upload-icon {
  width: 40px;
  height: 40px;
  border: 1px solid #DDD;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 15px;
  color: #999;
}

.upload-title {
  font-weight: 500;
  font-size: 0.9rem;
  margin-bottom: 5px;
}

.upload-hint {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: #999;
}

.file-list {
  width: 100%;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.file-item {
  display: flex;
  align-items: center;
  background: var(--white);
  padding: 8px 12px;
  border: 1px solid #EEE;
  font-family: var(--font-mono);
  font-size: 0.85rem;
}

.file-name {
  flex: 1;
  margin: 0 10px;
}

.remove-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  color: #999;
}

.console-divider {
  display: flex;
  align-items: center;
  margin: 10px 0;
}

.console-divider::before,
.console-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #EEE;
}

.console-divider span {
  padding: 0 15px;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: #BBB;
  letter-spacing: 1px;
}

.input-wrapper {
  position: relative;
  border: 1px solid #DDD;
  background: #FAFAFA;
}

.code-input {
  width: 100%;
  border: none;
  background: transparent;
  padding: 20px;
  font-family: var(--font-mono);
  font-size: 0.9rem;
  line-height: 1.6;
  resize: vertical;
  outline: none;
  min-height: 150px;
}

.model-badge {
  position: absolute;
  bottom: 10px;
  right: 15px;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: #AAA;
}

.start-engine-btn {
  width: 100%;
  background: var(--black);
  color: var(--white);
  border: none;
  padding: 20px;
  font-family: var(--font-mono);
  font-weight: 700;
  font-size: 1.1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 1px;
  position: relative;
  overflow: hidden;
}

/* Estado clickeable (no deshabilitado) */
.start-engine-btn:not(:disabled) {
  background: var(--black);
  border: 1px solid var(--black);
  animation: pulse-border 2s infinite;
}

.start-engine-btn:hover:not(:disabled) {
  background: var(--orange);
  border-color: var(--orange);
  transform: translateY(-2px);
}

.start-engine-btn:active:not(:disabled) {
  transform: translateY(0);
}

.start-engine-btn:disabled {
  background: #E5E5E5;
  color: #999;
  cursor: not-allowed;
  transform: none;
  border: 1px solid #E5E5E5;
}

/* Animación de guía: pulso sutil del borde */
@keyframes pulse-border {
  0% { box-shadow: 0 0 0 0 rgba(0, 0, 0, 0.2); }
  70% { box-shadow: 0 0 0 6px rgba(0, 0, 0, 0); }
  100% { box-shadow: 0 0 0 0 rgba(0, 0, 0, 0); }
}

/* Créditos footer */
.credits-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 28px 0 8px 0;
  border-top: 1px solid #F0F0F0;
  margin-top: 48px;
  flex-wrap: wrap;
}

.credits-text {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: #BBB;
  letter-spacing: 0.3px;
}

.credits-text strong {
  color: #999;
  font-weight: 600;
}

.credits-links {
  display: flex;
  align-items: center;
  gap: 12px;
}

.credits-link {
  color: #CCC;
  display: flex;
  align-items: center;
  transition: color 0.2s ease;
  text-decoration: none;
}

.credits-link:hover {
  color: #666;
}

/* Adaptación responsive */
@media (max-width: 1024px) {
  .dashboard-section {
    flex-direction: column;
  }
  
  .hero-section {
    flex-direction: column;
  }
  
  .hero-left {
    padding-right: 0;
    margin-bottom: 40px;
  }
  
  .hero-logo {
    max-width: 200px;
    margin-bottom: 20px;
  }
}
</style>
