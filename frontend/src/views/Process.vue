<template>
  <div class="process-page">
    <!-- Barra de navegación superior -->
    <nav class="navbar">
      <div class="nav-brand" @click="goHome">MIROFISH</div>
      
      <!-- Indicador de pasos central -->
      <div class="nav-center">
        <div class="step-badge">STEP 01</div>
        <div class="step-name">Construcción del grafo</div>
      </div>

      <div class="nav-status">
        <span class="status-dot" :class="statusClass"></span>
        <span class="status-text">{{ statusText }}</span>
      </div>
    </nav>

    <!-- Área de contenido principal -->
    <div class="main-content">
      <!-- Panel izquierdo: visualización del grafo en tiempo real -->
      <div class="left-panel" :class="{ 'full-screen': isFullScreen }">
        <div class="panel-header">
          <div class="header-left">
            <span class="header-deco">◆</span>
            <span class="header-title">Grafo de conocimiento en tiempo real</span>
          </div>
          <div class="header-right">
            <template v-if="graphData">
              <span class="stat-item">{{ graphData.node_count || graphData.nodes?.length || 0 }} nodos</span>
              <span class="stat-divider">|</span>
              <span class="stat-item">{{ graphData.edge_count || graphData.edges?.length || 0 }} relaciones</span>
              <span class="stat-divider">|</span>
            </template>
            <div class="action-buttons">
                <button class="action-btn" @click="refreshGraph" :disabled="graphLoading" title="Actualizar grafo">
                  <span class="icon-refresh" :class="{ 'spinning': graphLoading }">↻</span>
                </button>
                <button class="action-btn" @click="toggleFullScreen" :title="isFullScreen ? 'Salir de pantalla completa' : 'Pantalla completa'">
                  <span class="icon-fullscreen">{{ isFullScreen ? '↙' : '↗' }}</span>
                </button>
            </div>
          </div>
        </div>
        
        <div class="graph-container" ref="graphContainer">
          <!-- Visualización del grafo (se muestra siempre que haya datos) -->
          <div v-if="graphData" class="graph-view">
            <svg ref="graphSvg" class="graph-svg"></svg>
            <!-- Indicador de construcción en curso -->
            <div v-if="currentPhase === 1" class="graph-building-hint">
              <span class="building-dot"></span>
              Actualizando en tiempo real...
            </div>
            
            <!-- Panel de detalles de nodo/arista -->
            <div v-if="selectedItem" class="detail-panel">
              <div class="detail-panel-header">
                <span class="detail-title">{{ selectedItem.type === 'node' ? 'Node Details' : 'Relationship' }}</span>
                <span v-if="selectedItem.type === 'node'" class="detail-badge" :style="{ background: selectedItem.color }">
                  {{ selectedItem.entityType }}
                </span>
                <button class="detail-close" @click="closeDetailPanel">×</button>
              </div>
              
              <!-- Detalles del nodo -->
              <div v-if="selectedItem.type === 'node'" class="detail-content">
                <div class="detail-row">
                  <span class="detail-label">Name:</span>
                  <span class="detail-value highlight">{{ selectedItem.data.name }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">UUID:</span>
                  <span class="detail-value uuid">{{ selectedItem.data.uuid }}</span>
                </div>
                <div class="detail-row" v-if="selectedItem.data.created_at">
                  <span class="detail-label">Created:</span>
                  <span class="detail-value">{{ formatDate(selectedItem.data.created_at) }}</span>
                </div>
                
                <!-- Properties / Attributes -->
                <div class="detail-section" v-if="selectedItem.data.attributes && Object.keys(selectedItem.data.attributes).length > 0">
                  <span class="detail-label">Properties:</span>
                  <div class="properties-list">
                    <div v-for="(value, key) in selectedItem.data.attributes" :key="key" class="property-item">
                      <span class="property-key">{{ key }}:</span>
                      <span class="property-value">{{ value }}</span>
                    </div>
                  </div>
                </div>
                
                <!-- Summary -->
                <div class="detail-section" v-if="selectedItem.data.summary">
                  <span class="detail-label">Summary:</span>
                  <p class="detail-summary">{{ selectedItem.data.summary }}</p>
                </div>
                
                <!-- Labels -->
                <div class="detail-row" v-if="selectedItem.data.labels?.length">
                  <span class="detail-label">Labels:</span>
                  <div class="detail-labels">
                    <span v-for="label in selectedItem.data.labels" :key="label" class="label-tag">{{ label }}</span>
                  </div>
                </div>
              </div>
              
              <!-- Detalles de la arista -->
              <div v-else class="detail-content">
                <!-- Visualización de relaciones -->
                <div class="edge-relation">
                  <span class="edge-source">{{ selectedItem.data.source_name || selectedItem.data.source_node_name }}</span>
                  <span class="edge-arrow">→</span>
                  <span class="edge-type">{{ selectedItem.data.name || selectedItem.data.fact_type || 'RELATED_TO' }}</span>
                  <span class="edge-arrow">→</span>
                  <span class="edge-target">{{ selectedItem.data.target_name || selectedItem.data.target_node_name }}</span>
                </div>
                
                <div class="detail-subtitle">Relationship</div>
                
                <div class="detail-row">
                  <span class="detail-label">UUID:</span>
                  <span class="detail-value uuid">{{ selectedItem.data.uuid }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">Label:</span>
                  <span class="detail-value">{{ selectedItem.data.name || selectedItem.data.fact_type || 'RELATED_TO' }}</span>
                </div>
                <div class="detail-row" v-if="selectedItem.data.fact_type">
                  <span class="detail-label">Type:</span>
                  <span class="detail-value">{{ selectedItem.data.fact_type }}</span>
                </div>
                
                <!-- Fact -->
                <div class="detail-section" v-if="selectedItem.data.fact">
                  <span class="detail-label">Fact:</span>
                  <p class="detail-summary">{{ selectedItem.data.fact }}</p>
                </div>
                
                <!-- Episodes -->
                <div class="detail-section" v-if="selectedItem.data.episodes?.length">
                  <span class="detail-label">Episodes:</span>
                  <div class="episodes-list">
                    <span v-for="ep in selectedItem.data.episodes" :key="ep" class="episode-tag">{{ ep }}</span>
                  </div>
                </div>
                
                <div class="detail-row" v-if="selectedItem.data.created_at">
                  <span class="detail-label">Created:</span>
                  <span class="detail-value">{{ formatDate(selectedItem.data.created_at) }}</span>
                </div>
                <div class="detail-row" v-if="selectedItem.data.valid_at">
                  <span class="detail-label">Valid From:</span>
                  <span class="detail-value">{{ formatDate(selectedItem.data.valid_at) }}</span>
                </div>
                <div class="detail-row" v-if="selectedItem.data.invalid_at">
                  <span class="detail-label">Invalid At:</span>
                  <span class="detail-value">{{ formatDate(selectedItem.data.invalid_at) }}</span>
                </div>
                <div class="detail-row" v-if="selectedItem.data.expired_at">
                  <span class="detail-label">Expired At:</span>
                  <span class="detail-value">{{ formatDate(selectedItem.data.expired_at) }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Estado de carga -->
          <div v-else-if="graphLoading" class="graph-loading">
            <div class="loading-animation">
              <div class="loading-ring"></div>
              <div class="loading-ring"></div>
              <div class="loading-ring"></div>
            </div>
            <p class="loading-text">Cargando datos del grafo...</p>
          </div>
          
          <!-- Esperando construcción -->
          <div v-else-if="currentPhase < 1" class="graph-waiting">
            <div class="waiting-icon">
              <svg viewBox="0 0 100 100" class="network-icon">
                <circle cx="50" cy="20" r="8" fill="none" stroke="#000" stroke-width="1.5"/>
                <circle cx="20" cy="60" r="8" fill="none" stroke="#000" stroke-width="1.5"/>
                <circle cx="80" cy="60" r="8" fill="none" stroke="#000" stroke-width="1.5"/>
                <circle cx="50" cy="80" r="8" fill="none" stroke="#000" stroke-width="1.5"/>
                <line x1="50" y1="28" x2="25" y2="54" stroke="#000" stroke-width="1"/>
                <line x1="50" y1="28" x2="75" y2="54" stroke="#000" stroke-width="1"/>
                <line x1="28" y1="60" x2="72" y2="60" stroke="#000" stroke-width="1" stroke-dasharray="4"/>
                <line x1="50" y1="72" x2="26" y2="66" stroke="#000" stroke-width="1"/>
                <line x1="50" y1="72" x2="74" y2="66" stroke="#000" stroke-width="1"/>
              </svg>
            </div>
            <p class="waiting-text">Esperando generación de ontología</p>
            <p class="waiting-hint">La construcción del grafo comenzará automáticamente al finalizar</p>
          </div>
          
          <!-- Construyendo, sin datos aún -->
          <div v-else-if="currentPhase === 1 && !graphData" class="graph-waiting">
            <div class="loading-animation">
              <div class="loading-ring"></div>
              <div class="loading-ring"></div>
              <div class="loading-ring"></div>
            </div>
            <p class="waiting-text">Construyendo grafo</p>
            <p class="waiting-hint">Los datos aparecerán en breve...</p>
          </div>
          
          <!-- Estado de error -->
          <div v-else-if="error" class="graph-error">
            <span class="error-icon">⚠</span>
            <p>{{ error }}</p>
          </div>
        </div>
        
        <!-- Leyenda del grafo -->
        <div v-if="graphData" class="graph-legend">
          <div class="legend-item" v-for="type in entityTypes" :key="type.name">
            <span class="legend-dot" :style="{ background: type.color }"></span>
            <span class="legend-label">{{ type.name }}</span>
            <span class="legend-count">{{ type.count }}</span>
          </div>
        </div>
      </div>

      <!-- Panel derecho: detalles del proceso de construcción -->
      <div class="right-panel" :class="{ 'hidden': isFullScreen }">
        <div class="panel-header dark-header">
          <span class="header-icon">▣</span>
          <span class="header-title">Proceso de construcción</span>
        </div>

        <div class="process-content">
          <!-- Fase 1: generación de ontología -->
          <div class="process-phase" :class="{ 'active': currentPhase === 0, 'completed': currentPhase > 0 }">
            <div class="phase-header">
              <span class="phase-num">01</span>
              <div class="phase-info">
                <div class="phase-title">Generación de ontología</div>
                <div class="phase-api">/api/graph/ontology/generate</div>
              </div>
              <span class="phase-status" :class="getPhaseStatusClass(0)">
                {{ getPhaseStatusText(0) }}
              </span>
            </div>
            
            <div class="phase-detail">
              <div class="detail-section">
                <div class="detail-label">Descripción de la API</div>
                <div class="detail-content">
                  Tras subir el documento, el LLM analiza el contenido y genera automáticamente una estructura ontológica adecuada para la simulación de opinión pública (tipos de entidades + tipos de relaciones)
                </div>
              </div>
              
              <!-- Progreso de generación de ontología -->
              <div class="detail-section" v-if="ontologyProgress && currentPhase === 0">
                <div class="detail-label">Progreso de generación</div>
                <div class="ontology-progress">
                  <div class="progress-spinner"></div>
                  <span class="progress-text">{{ ontologyProgress.message }}</span>
                </div>
              </div>
              
              <!-- Información de ontología generada -->
              <div class="detail-section" v-if="projectData?.ontology">
                <div class="detail-label">Tipos de entidades generados ({{ projectData.ontology.entity_types?.length || 0 }})</div>
                <div class="entity-tags">
                  <span 
                    v-for="entity in projectData.ontology.entity_types" 
                    :key="entity.name"
                    class="entity-tag"
                  >
                    {{ entity.name }}
                  </span>
                </div>
              </div>
              
              <div class="detail-section" v-if="projectData?.ontology">
                <div class="detail-label">Tipos de relaciones generados ({{ projectData.ontology.relation_types?.length || 0 }})</div>
                <div class="relation-list">
                  <div 
                    v-for="(rel, idx) in projectData.ontology.relation_types?.slice(0, 5) || []" 
                    :key="idx"
                    class="relation-item"
                  >
                    <span class="rel-source">{{ rel.source_type }}</span>
                    <span class="rel-arrow">→</span>
                    <span class="rel-name">{{ rel.name }}</span>
                    <span class="rel-arrow">→</span>
                    <span class="rel-target">{{ rel.target_type }}</span>
                  </div>
                  <div v-if="(projectData.ontology.relation_types?.length || 0) > 5" class="relation-more">
                    +{{ projectData.ontology.relation_types.length - 5 }} más...
                  </div>
                </div>
              </div>
              
              <!-- Estado de espera -->
              <div class="detail-section waiting-state" v-if="!projectData?.ontology && currentPhase === 0 && !ontologyProgress">
                <div class="waiting-hint">Esperando generación de ontología...</div>
              </div>
            </div>
          </div>

          <!-- Fase 2: construcción del grafo -->
          <div class="process-phase" :class="{ 'active': currentPhase === 1, 'completed': currentPhase > 1 }">
            <div class="phase-header">
              <span class="phase-num">02</span>
              <div class="phase-info">
                <div class="phase-title">Construcción del grafo</div>
                <div class="phase-api">/api/graph/build</div>
              </div>
              <span class="phase-status" :class="getPhaseStatusClass(1)">
                {{ getPhaseStatusText(1) }}
              </span>
            </div>
            
            <div class="phase-detail">
              <div class="detail-section">
                <div class="detail-label">Descripción de la API</div>
                <div class="detail-content">
                  Basándose en la ontología generada, divide el documento en fragmentos y llama a la API de Zep para construir el grafo de conocimiento, extrayendo entidades y relaciones
                </div>
              </div>
              
              <!-- Esperando finalización de ontología -->
              <div class="detail-section waiting-state" v-if="currentPhase < 1">
                <div class="waiting-hint">Esperando que finalice la generación de ontología...</div>
              </div>
              
              <!-- Progreso de construcción -->
              <div class="detail-section" v-if="buildProgress && currentPhase >= 1">
                <div class="detail-label">Progreso de construcción</div>
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: buildProgress.progress + '%' }"></div>
                </div>
                <div class="progress-info">
                  <span class="progress-message">{{ buildProgress.message }}</span>
                  <span class="progress-percent">{{ buildProgress.progress }}%</span>
                </div>
              </div>
              
              <div class="detail-section" v-if="graphData">
                <div class="detail-label">Resultado de construcción</div>
                <div class="build-result">
                  <div class="result-item">
                    <span class="result-value">{{ graphData.node_count }}</span>
                    <span class="result-label">Nodos de entidad</span>
                  </div>
                  <div class="result-item">
                    <span class="result-value">{{ graphData.edge_count }}</span>
                    <span class="result-label">Aristas de relación</span>
                  </div>
                  <div class="result-item">
                    <span class="result-value">{{ entityTypes.length }}</span>
                    <span class="result-label">Tipos de entidad</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Fase 3: completado -->
          <div class="process-phase" :class="{ 'active': currentPhase === 2, 'completed': currentPhase > 2 }">
            <div class="phase-header">
              <span class="phase-num">03</span>
              <div class="phase-info">
                <div class="phase-title">Construcción completada</div>
                <div class="phase-api">Listo para el siguiente paso</div>
              </div>
              <span class="phase-status" :class="getPhaseStatusClass(2)">
                {{ getPhaseStatusText(2) }}
              </span>
            </div>
          </div>

          <!-- Botón de siguiente paso -->
          <div class="next-step-section" v-if="currentPhase >= 2">
            <button class="next-step-btn" @click="goToNextStep" :disabled="currentPhase < 2">
              Ir a configuración del entorno
              <span class="btn-arrow">→</span>
            </button>
          </div>
        </div>

        <!-- Panel de información del proyecto -->
        <div class="project-panel">
          <div class="project-header">
            <span class="project-icon">◇</span>
            <span class="project-title">Información del proyecto</span>
          </div>
          <div class="project-details" v-if="projectData">
            <div class="project-item">
              <span class="item-label">Nombre del proyecto</span>
              <span class="item-value">{{ projectData.name }}</span>
            </div>
            <div class="project-item">
              <span class="item-label">ID del proyecto</span>
              <span class="item-value code">{{ projectData.project_id }}</span>
            </div>
            <div class="project-item" v-if="projectData.graph_id">
              <span class="item-label">ID del grafo</span>
              <span class="item-value code">{{ projectData.graph_id }}</span>
            </div>
            <div class="project-item">
              <span class="item-label">Requisitos de simulación</span>
              <span class="item-value">{{ projectData.simulation_requirement || '-' }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { generateOntology, getProject, buildGraph, getTaskStatus, getGraphData } from '../api/graph'
import { getPendingUpload, clearPendingUpload } from '../store/pendingUpload'
import * as d3 from 'd3'

const route = useRoute()
const router = useRouter()

// ID del proyecto actual (puede cambiar de 'new' a ID real)
const currentProjectId = ref(route.params.projectId)

// Estado
const loading = ref(true)
const graphLoading = ref(false)
const error = ref('')
const projectData = ref(null)
const graphData = ref(null)
const buildProgress = ref(null)
const ontologyProgress = ref(null) // Progreso de generación de ontología
const currentPhase = ref(-1) // -1: subiendo, 0: generando ontología, 1: construyendo grafo, 2: completado
const selectedItem = ref(null) // Nodo o arista seleccionado
const isFullScreen = ref(false)

// Referencias DOM
const graphContainer = ref(null)
const graphSvg = ref(null)

// Temporizadores de sondeo
let pollTimer = null

// Propiedades computadas
const statusClass = computed(() => {
  if (error.value) return 'error'
  if (currentPhase.value >= 2) return 'completed'
  return 'processing'
})

const statusText = computed(() => {
  if (error.value) return 'Construcción fallida'
  if (currentPhase.value >= 2) return 'Construcción completada'
  if (currentPhase.value === 1) return 'Construyendo grafo'
  if (currentPhase.value === 0) return 'Generando ontología'
  return 'Inicializando'
})

const entityTypes = computed(() => {
  if (!graphData.value?.nodes) return []
  
  const typeMap = {}
  const colors = ['#FF6B35', '#004E89', '#7B2D8E', '#1A936F', '#C5283D', '#E9724C']
  
  graphData.value.nodes.forEach(node => {
    const type = node.labels?.find(l => l !== 'Entity') || 'Entity'
    if (!typeMap[type]) {
      typeMap[type] = { name: type, count: 0, color: colors[Object.keys(typeMap).length % colors.length] }
    }
    typeMap[type].count++
  })
  
  return Object.values(typeMap)
})

// Métodos
const goHome = () => {
  router.push('/')
}

const goToNextStep = () => {
  // TODO: ir al paso de configuración del entorno
  alert('Función de configuración del entorno en desarrollo...')
}

const toggleFullScreen = () => {
  isFullScreen.value = !isFullScreen.value
  // Wait for transition to finish then re-render graph
  setTimeout(() => {
    renderGraph()
  }, 350) 
}

// Cerrar panel de detalles
const closeDetailPanel = () => {
  selectedItem.value = null
}

// Formatear fecha
const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  try {
    const date = new Date(dateStr)
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return dateStr
  }
}

// Seleccionar nodo
const selectNode = (nodeData, color) => {
  selectedItem.value = {
    type: 'node',
    data: nodeData,
    color: color,
    entityType: nodeData.labels?.find(l => l !== 'Entity' && l !== 'Node') || 'Entity'
  }
}

// Seleccionar arista
const selectEdge = (edgeData) => {
  selectedItem.value = {
    type: 'edge',
    data: edgeData
  }
}

const getPhaseStatusClass = (phase) => {
  if (currentPhase.value > phase) return 'completed'
  if (currentPhase.value === phase) return 'active'
  return 'pending'
}

const getPhaseStatusText = (phase) => {
  if (currentPhase.value > phase) return 'Completado'
  if (currentPhase.value === phase) {
    if (phase === 1 && buildProgress.value) {
      return `${buildProgress.value.progress}%`
    }
    return 'En progreso'
  }
  return 'Esperando'
}

// Inicialización - manejar nuevo proyecto o cargar existente
const initProject = async () => {
  const paramProjectId = route.params.projectId
  
  if (paramProjectId === 'new') {
    // Nuevo proyecto: obtener datos pendientes de subir desde el store
    await handleNewProject()
  } else {
    // Cargar proyecto existente
    currentProjectId.value = paramProjectId
    await loadProject()
  }
}

// Manejar nuevo proyecto - llamar a API ontology/generate
const handleNewProject = async () => {
  const pending = getPendingUpload()
  
  if (!pending.isPending || pending.files.length === 0) {
    error.value = 'No hay archivos pendientes de subir, vuelve a la página principal'
    loading.value = false
    return
  }
  
  try {
    loading.value = true
    currentPhase.value = 0 // Fase de generación de ontología
    ontologyProgress.value = { message: 'Subiendo archivo y analizando documento...' }
    
    // Construir FormData
    const formDataObj = new FormData()
    pending.files.forEach(file => {
      formDataObj.append('files', file)
    })
    formDataObj.append('simulation_requirement', pending.simulationRequirement)
    
    // Llamar a la API de generación de ontología
    const response = await generateOntology(formDataObj)
    
    if (response.success) {
      // Limpiar datos pendientes de subir
      clearPendingUpload()
      
      // Actualizar ID y datos del proyecto
      currentProjectId.value = response.data.project_id
      projectData.value = response.data
      
      // Actualizar URL (sin recargar la página)
      router.replace({
        name: 'Process',
        params: { projectId: response.data.project_id }
      })
      
      ontologyProgress.value = null
      
      // Iniciar construcción del grafo automáticamente
      await startBuildGraph()
    } else {
      error.value = response.error || 'Falló la generación de ontología'
    }
  } catch (err) {
    console.error('Handle new project error:', err)
    error.value = 'Error al inicializar proyecto: ' + (err.message || 'Error desconocido')
  } finally {
    loading.value = false
  }
}

// Cargar datos del proyecto existente
const loadProject = async () => {
  try {
    loading.value = true
    const response = await getProject(currentProjectId.value)
    
    if (response.success) {
      projectData.value = response.data
      updatePhaseByStatus(response.data.status)
      
      // Iniciar construcción del grafo automáticamente
      if (response.data.status === 'ontology_generated' && !response.data.graph_id) {
        await startBuildGraph()
      }
      
      // Continuar sondeo de tareas en construcción
      if (response.data.status === 'graph_building' && response.data.graph_build_task_id) {
        currentPhase.value = 1
        startPollingTask(response.data.graph_build_task_id)
      }
      
      // Cargar grafo completado
      if (response.data.status === 'graph_completed' && response.data.graph_id) {
        currentPhase.value = 2
        await loadGraph(response.data.graph_id)
      }
    } else {
      error.value = response.error || 'Error al cargar proyecto'
    }
  } catch (err) {
    console.error('Load project error:', err)
    error.value = 'Error al cargar proyecto: ' + (err.message || 'Error desconocido')
  } finally {
    loading.value = false
  }
}

const updatePhaseByStatus = (status) => {
  switch (status) {
    case 'created':
    case 'ontology_generated':
      currentPhase.value = 0
      break
    case 'graph_building':
      currentPhase.value = 1
      break
    case 'graph_completed':
      currentPhase.value = 2
      break
    case 'failed':
      error.value = projectData.value?.error || 'Error de procesamiento'
      break
  }
}

// Iniciar construcción del grafo
const startBuildGraph = async () => {
  try {
    currentPhase.value = 1
    // Establecer progreso inicial
    buildProgress.value = {
      progress: 0,
      message: 'Iniciando construcción del grafo...'
    }
    
    const response = await buildGraph({ project_id: currentProjectId.value })
    
    if (response.success) {
      buildProgress.value.message = 'Tarea de construcción del grafo iniciada...'
      
      // Guardar task_id para sondeo
      const taskId = response.data.task_id
      
      // Iniciar sondeo de datos del grafo (independiente del sondeo de estado de tarea)
      startGraphPolling()
      
      // Iniciar sondeo de estado de tarea
      startPollingTask(taskId)
    } else {
      error.value = response.error || 'Error al iniciar construcción del grafo'
      buildProgress.value = null
    }
  } catch (err) {
    console.error('Build graph error:', err)
    error.value = 'Error al iniciar construcción del grafo: ' + (err.message || 'Error desconocido')
    buildProgress.value = null
  }
}

// Temporizador de sondeo de datos del grafo
let graphPollTimer = null

// Iniciar sondeo de datos del grafo
const startGraphPolling = () => {
  // Obtener datos inmediatamente
  fetchGraphData()
  
  // Obtener datos del grafo automáticamente cada 10 segundos
  graphPollTimer = setInterval(async () => {
    await fetchGraphData()
  }, 10000)
}

// Actualizar grafo manualmente
const refreshGraph = async () => {
  graphLoading.value = true
  await fetchGraphData()
  graphLoading.value = false
}

// Detener sondeo de datos del grafo
const stopGraphPolling = () => {
  if (graphPollTimer) {
    clearInterval(graphPollTimer)
    graphPollTimer = null
  }
}

// Obtener datos del grafo
const fetchGraphData = async () => {
  try {
    // Primero obtener info del proyecto para obtener graph_id
    const projectResponse = await getProject(currentProjectId.value)
    
    if (projectResponse.success && projectResponse.data.graph_id) {
      const graphId = projectResponse.data.graph_id
      projectData.value = projectResponse.data
      
      // Obtener datos del grafo
      const graphResponse = await getGraphData(graphId)
      
      if (graphResponse.success && graphResponse.data) {
        const newData = graphResponse.data
        const newNodeCount = newData.node_count || newData.nodes?.length || 0
        const oldNodeCount = graphData.value?.node_count || graphData.value?.nodes?.length || 0
        
        console.log('Fetching graph data, nodes:', newNodeCount, 'edges:', newData.edge_count || newData.edges?.length || 0)
        
        // Actualizar renderizado cuando cambian los datos
        if (newNodeCount !== oldNodeCount || !graphData.value) {
          graphData.value = newData
          await nextTick()
          renderGraph()
        }
      }
    }
  } catch (err) {
    console.log('Graph data fetch:', err.message || 'not ready')
  }
}

// Sondear estado de tarea
const startPollingTask = (taskId) => {
  // Ejecutar consulta inmediatamente
  pollTaskStatus(taskId)
  
  // Luego sondear periódicamente
  pollTimer = setInterval(() => {
    pollTaskStatus(taskId)
  }, 2000)
}

// Consultar estado de tarea
const pollTaskStatus = async (taskId) => {
  try {
    const response = await getTaskStatus(taskId)
    
    if (response.success) {
      const task = response.data
      
      // Actualizar visualización de progreso
      buildProgress.value = {
        progress: task.progress || 0,
        message: task.message || 'Procesando...'
      }
      
      console.log('Task status:', task.status, 'Progress:', task.progress)
      
      if (task.status === 'completed') {
        console.log('✅ Construcción del grafo completada, cargando datos completos...')
        
        stopPolling()
        stopGraphPolling()
        currentPhase.value = 2
        
        // Actualizar visualización de progreso al estado completado
        buildProgress.value = {
          progress: 100,
          message: 'Construcción completada, cargando grafo...'
        }
        
        // Recargar datos del proyecto para obtener graph_id
        const projectResponse = await getProject(currentProjectId.value)
        if (projectResponse.success) {
          projectData.value = projectResponse.data
          
          // Carga final de datos completos del grafo
          if (projectResponse.data.graph_id) {
            console.log('📊 Cargando grafo completo:', projectResponse.data.graph_id)
            await loadGraph(projectResponse.data.graph_id)
            console.log('✅ Grafo cargado correctamente')
          }
        }
        
        // Limpiar visualización de progreso
        buildProgress.value = null
      } else if (task.status === 'failed') {
        stopPolling()
        stopGraphPolling()
        error.value = 'Error en construcción del grafo: ' + (task.error || 'Error desconocido')
        buildProgress.value = null
      }
    }
  } catch (err) {
    console.error('Poll task error:', err)
  }
}

const stopPolling = () => {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
}

// Cargar datos del grafo
const loadGraph = async (graphId) => {
  try {
    graphLoading.value = true
    const response = await getGraphData(graphId)
    
    if (response.success) {
      graphData.value = response.data
      await nextTick()
      renderGraph()
    }
  } catch (err) {
    console.error('Load graph error:', err)
  } finally {
    graphLoading.value = false
  }
}

// Renderizar grafo (D3.js)
const renderGraph = () => {
  if (!graphSvg.value || !graphData.value) {
    console.log('Cannot render: svg or data missing')
    return
  }
  
  const container = graphContainer.value
  if (!container) {
    console.log('Cannot render: container missing')
    return
  }
  
  // Obtener dimensiones del contenedor
  const rect = container.getBoundingClientRect()
  const width = rect.width || 800
  const height = (rect.height || 600) - 60
  
  if (width <= 0 || height <= 0) {
    console.log('Cannot render: invalid dimensions', width, height)
    return
  }
  
  console.log('Rendering graph:', width, 'x', height)
  
  const svg = d3.select(graphSvg.value)
    .attr('width', width)
    .attr('height', height)
    .attr('viewBox', `0 0 ${width} ${height}`)
  
  svg.selectAll('*').remove()
  
  // Procesar datos de nodos
  const nodesData = graphData.value.nodes || []
  const edgesData = graphData.value.edges || []
  
  if (nodesData.length === 0) {
    console.log('No nodes to render')
    // Mostrar estado vacío
    svg.append('text')
      .attr('x', width / 2)
      .attr('y', height / 2)
      .attr('text-anchor', 'middle')
      .attr('fill', '#999')
      .text('Esperando datos del grafo...')
    return
  }
  
  // Crear mapa de nodos para buscar nombres
  const nodeMap = {}
  nodesData.forEach(n => {
    nodeMap[n.uuid] = n
  })
  
  const nodes = nodesData.map(n => ({
    id: n.uuid,
    name: n.name || 'Sin nombre',
    type: n.labels?.find(l => l !== 'Entity' && l !== 'Node') || 'Entity',
    rawData: n // Guardar datos originales
  }))
  
  // Crear conjunto de IDs de nodos para filtrar aristas válidas
  const nodeIds = new Set(nodes.map(n => n.id))
  
  const edges = edgesData
    .filter(e => nodeIds.has(e.source_node_uuid) && nodeIds.has(e.target_node_uuid))
    .map(e => ({
      source: e.source_node_uuid,
      target: e.target_node_uuid,
      type: e.fact_type || e.name || 'RELATED_TO',
      rawData: {
        ...e,
        source_name: nodeMap[e.source_node_uuid]?.name || 'Desconocido',
        target_name: nodeMap[e.target_node_uuid]?.name || 'Desconocido'
      }
    }))
  
  console.log('Nodes:', nodes.length, 'Edges:', edges.length)
  
  // Mapeo de colores
  const types = [...new Set(nodes.map(n => n.type))]
  const colorScale = d3.scaleOrdinal()
    .domain(types)
    .range(['#FF6B35', '#004E89', '#7B2D8E', '#1A936F', '#C5283D', '#E9724C', '#2D3436', '#6C5CE7'])
  
  // Diseño de fuerza dirigida
  const simulation = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(edges).id(d => d.id).distance(100).strength(0.5))
    .force('charge', d3.forceManyBody().strength(-300))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('collision', d3.forceCollide().radius(40))
    .force('x', d3.forceX(width / 2).strength(0.05))
    .force('y', d3.forceY(height / 2).strength(0.05))
  
  // Agregar funcionalidad de zoom
  const g = svg.append('g')
  
  svg.call(d3.zoom()
    .extent([[0, 0], [width, height]])
    .scaleExtent([0.2, 4])
    .on('zoom', (event) => {
      g.attr('transform', event.transform)
    }))
  
  // Dibujar aristas (con línea transparente ancha para clic)
  const linkGroup = g.append('g')
    .attr('class', 'links')
    .selectAll('g')
    .data(edges)
    .enter()
    .append('g')
    .style('cursor', 'pointer')
    .on('click', (event, d) => {
      event.stopPropagation()
      selectEdge(d.rawData)
    })
  
  // Línea delgada visible
  const link = linkGroup.append('line')
    .attr('stroke', '#ccc')
    .attr('stroke-width', 1.5)
    .attr('stroke-opacity', 0.6)
  
  // Línea ancha transparente para área de clic
  linkGroup.append('line')
    .attr('stroke', 'transparent')
    .attr('stroke-width', 10)
  
  // Etiquetas de arista
  const linkLabel = g.append('g')
    .attr('class', 'link-labels')
    .selectAll('text')
    .data(edges)
    .enter()
    .append('text')
    .attr('font-size', '9px')
    .attr('fill', '#999')
    .attr('text-anchor', 'middle')
    .text(d => d.type.length > 15 ? d.type.substring(0, 12) + '...' : d.type)
  
  // Dibujar nodos
  const node = g.append('g')
    .attr('class', 'nodes')
    .selectAll('g')
    .data(nodes)
    .enter()
    .append('g')
    .style('cursor', 'pointer')
    .on('click', (event, d) => {
      event.stopPropagation()
      selectNode(d.rawData, colorScale(d.type))
    })
    .call(d3.drag()
      .on('start', dragstarted)
      .on('drag', dragged)
      .on('end', dragended))
  
  node.append('circle')
    .attr('r', 10)
    .attr('fill', d => colorScale(d.type))
    .attr('stroke', '#fff')
    .attr('stroke-width', 2)
    .attr('class', 'node-circle')
  
  node.append('text')
    .attr('dx', 14)
    .attr('dy', 4)
    .text(d => d.name?.substring(0, 12) || '')
    .attr('font-size', '11px')
    .attr('fill', '#333')
    .attr('font-family', 'JetBrains Mono, monospace')
  
  // Clic en área vacía para cerrar panel de detalles
  svg.on('click', () => {
    closeDetailPanel()
  })
  
  simulation.on('tick', () => {
    // Actualizar posición de todas las aristas (incluyendo línea visible y área de clic transparente)
    linkGroup.selectAll('line')
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y)
    
    // Actualizar posición de etiquetas de arista
    linkLabel
      .attr('x', d => (d.source.x + d.target.x) / 2)
      .attr('y', d => (d.source.y + d.target.y) / 2 - 5)
    
    node.attr('transform', d => `translate(${d.x},${d.y})`)
  })
  
  function dragstarted(event) {
    if (!event.active) simulation.alphaTarget(0.3).restart()
    event.subject.fx = event.subject.x
    event.subject.fy = event.subject.y
  }
  
  function dragged(event) {
    event.subject.fx = event.x
    event.subject.fy = event.y
  }
  
  function dragended(event) {
    if (!event.active) simulation.alphaTarget(0)
    event.subject.fx = null
    event.subject.fy = null
  }
}

// Observar cambios en datos del grafo
watch(graphData, () => {
  if (graphData.value) {
    nextTick(() => renderGraph())
  }
})

// Ciclo de vida
onMounted(() => {
  initProject()
})

onUnmounted(() => {
  stopPolling()
  stopGraphPolling()
})
</script>

<style scoped>
/* Variables */
:root {
  --black: #000000;
  --white: #FFFFFF;
  --orange: #FF6B35;
  --gray-light: #F5F5F5;
  --gray-border: #E0E0E0;
  --gray-text: #666666;
}

.process-page {
  min-height: 100vh;
  background: var(--white);
  font-family: 'JetBrains Mono', 'Noto Sans SC', monospace;
  overflow: hidden; /* Prevent body scroll in fullscreen */
}

/* Barra de navegación */
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 56px;
  background: #000;
  color: #fff;
  z-index: 10;
  position: relative;
}

.nav-brand {
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  cursor: pointer;
  transition: opacity 0.2s;
}

.nav-brand:hover {
  opacity: 0.8;
}

.nav-center {
  display: flex;
  align-items: center;
  gap: 12px;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

.step-badge {
  background: #FF6B35;
  color: #fff;
  padding: 2px 8px;
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  border-radius: 2px;
}

.step-name {
  font-size: 0.85rem;
  letter-spacing: 0.05em;
  color: #fff;
}

.nav-status {
  display: flex;
  align-items: center;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #666;
  margin-right: 8px;
}

.status-dot.processing {
  background: #FF6B35;
  animation: pulse 1.5s infinite;
}

.status-dot.completed {
  background: #1A936F;
}

.status-dot.error {
  background: #C5283D;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.status-text {
  font-size: 0.75rem;
  color: #999;
}

/* Área de contenido principal */
.main-content {
  display: flex;
  height: calc(100vh - 56px);
  position: relative;
}

/* Panel izquierdo - 50% predeterminado */
.left-panel {
  width: 50%;
  flex: none; /* Fixed width initially */
  display: flex;
  flex-direction: column;
  border-right: 1px solid #E0E0E0;
  transition: width 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  background: #fff;
  z-index: 5;
}

.left-panel.full-screen {
  width: 100%;
  border-right: none;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px;
  border-bottom: 1px solid #E0E0E0;
  background: #fff;
  height: 50px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-deco {
  color: #FF6B35;
  font-size: 0.8rem;
}

.header-title {
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 0.05em;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 0.75rem;
  color: #666;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.stat-val {
  font-weight: 600;
  color: #333;
}

.stat-divider {
  color: #eee;
}

.action-buttons {
    display: flex;
    align-items: center;
    gap: 8px;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background: transparent;
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.2s;
  color: #666;
  border-radius: 2px;
}

.action-btn:hover:not(:disabled) {
  background: #F5F5F5;
  color: #000;
}

.action-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.icon-refresh, .icon-fullscreen {
  font-size: 1rem;
  line-height: 1;
}

.icon-refresh.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Contenedor del grafo */
.graph-container {
  flex: 1;
  position: relative;
  overflow: hidden;
}

.graph-loading,
.graph-waiting,
.graph-error {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.loading-animation {
  position: relative;
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
}

.loading-ring {
  position: absolute;
  border: 2px solid transparent;
  border-radius: 50%;
  animation: ring-rotate 1.5s linear infinite;
}

.loading-ring:nth-child(1) {
  width: 80px;
  height: 80px;
  border-top-color: #000;
}

.loading-ring:nth-child(2) {
  width: 60px;
  height: 60px;
  top: 10px;
  left: 10px;
  border-right-color: #FF6B35;
  animation-delay: 0.2s;
}

.loading-ring:nth-child(3) {
  width: 40px;
  height: 40px;
  top: 20px;
  left: 20px;
  border-bottom-color: #666;
  animation-delay: 0.4s;
}

@keyframes ring-rotate {
  to { transform: rotate(360deg); }
}

.loading-text,
.waiting-text {
  font-size: 0.9rem;
  color: #333;
  margin: 0 0 8px;
}

.waiting-hint {
  font-size: 0.8rem;
  color: #999;
  margin: 0;
}

.waiting-icon {
  margin-bottom: 20px;
}

.network-icon {
  width: 100px;
  height: 100px;
  opacity: 0.6;
}

.graph-view {
  width: 100%;
  height: 100%;
  position: relative;
}

.graph-svg {
  width: 100%;
  height: 100%;
  display: block;
}

.graph-building-hint {
  position: absolute;
  bottom: 16px;
  left: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(255, 107, 53, 0.1);
  border: 1px solid #FF6B35;
  font-size: 0.8rem;
  color: #FF6B35;
}

.building-dot {
  width: 8px;
  height: 8px;
  background: #FF6B35;
  border-radius: 50%;
  animation: pulse 1s infinite;
}

/* Panel de detalles de nodo/arista */
.detail-panel {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 320px;
  max-height: calc(100% - 32px);
  background: #fff;
  border: 1px solid #E0E0E0;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  z-index: 100;
}

.detail-panel-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: #FAFAFA;
  border-bottom: 1px solid #E0E0E0;
}

.detail-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: #333;
}

.detail-badge {
  padding: 2px 10px;
  font-size: 0.75rem;
  color: #fff;
  border-radius: 2px;
}

.detail-close {
  margin-left: auto;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  font-size: 1.2rem;
  color: #999;
  cursor: pointer;
  transition: color 0.2s;
}

.detail-close:hover {
  color: #333;
}

.detail-content {
  padding: 16px;
  overflow-y: auto;
  flex: 1;
}

.detail-row {
  display: flex;
  align-items: flex-start;
  margin-bottom: 12px;
}

.detail-label {
  font-size: 0.8rem;
  color: #999;
  min-width: 70px;
  flex-shrink: 0;
}

.detail-value {
  font-size: 0.85rem;
  color: #333;
  word-break: break-word;
}

.detail-value.uuid {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: #666;
}

.detail-section {
  margin-bottom: 12px;
}

.detail-summary {
  margin: 8px 0 0 0;
  font-size: 0.85rem;
  color: #333;
  line-height: 1.6;
  padding: 10px;
  background: #F9F9F9;
  border-left: 3px solid #FF6B35;
}

.detail-labels {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.label-tag {
  padding: 2px 8px;
  font-size: 0.75rem;
  background: #F0F0F0;
  border: 1px solid #E0E0E0;
  color: #666;
}

/* Visualización de relaciones en detalle de arista */
.edge-relation {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
  padding: 12px;
  background: #F9F9F9;
  border: 1px solid #E0E0E0;
}

.edge-source,
.edge-target {
  font-size: 0.85rem;
  font-weight: 500;
  color: #333;
}

.edge-arrow {
  color: #999;
}

.edge-type {
  padding: 2px 8px;
  font-size: 0.75rem;
  background: #FF6B35;
  color: #fff;
}

.detail-value.highlight {
  font-weight: 600;
  color: #000;
}

.detail-subtitle {
  font-size: 0.9rem;
  font-weight: 600;
  color: #333;
  margin: 16px 0 12px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid #E0E0E0;
}

/* Lista de atributos/propiedades */
.properties-list {
  margin-top: 8px;
  padding: 10px;
  background: #F9F9F9;
  border: 1px solid #E0E0E0;
}

.property-item {
  display: flex;
  margin-bottom: 6px;
  font-size: 0.85rem;
}

.property-item:last-child {
  margin-bottom: 0;
}

.property-key {
  color: #666;
  margin-right: 8px;
  font-family: 'JetBrains Mono', monospace;
}

.property-value {
  color: #333;
  word-break: break-word;
}

/* Lista de episodios */
.episodes-list {
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.episode-tag {
  display: block;
  padding: 6px 10px;
  font-size: 0.75rem;
  font-family: 'JetBrains Mono', monospace;
  background: #F0F0F0;
  border: 1px solid #E0E0E0;
  color: #666;
  word-break: break-all;
}

.error-icon {
  font-size: 2rem;
  display: block;
  margin-bottom: 10px;
}

/* Leyenda del grafo */
.graph-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  padding: 12px 24px;
  border-top: 1px solid #E0E0E0;
  background: #FAFAFA;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.75rem;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.legend-label {
  color: #333;
}

.legend-count {
  color: #999;
}

/* Panel derecho - 50% predeterminado */
.right-panel {
  width: 50%;
  flex: none;
  display: flex;
  flex-direction: column;
  background: #fff;
  transition: width 0.35s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.3s ease, transform 0.3s ease;
  overflow: hidden;
  opacity: 1;
}

.right-panel.hidden {
  width: 0;
  opacity: 0;
  transform: translateX(20px);
  pointer-events: none;
}

.right-panel .panel-header.dark-header {
  background: #000;
  color: #fff;
  border-bottom: none;
}

.right-panel .header-icon {
  color: #FF6B35;
  margin-right: 8px;
}

/* Contenido del proceso */
.process-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

/* Fases del proceso */
.process-phase {
  margin-bottom: 24px;
  border: 1px solid #E0E0E0;
  opacity: 0.5;
  transition: all 0.3s;
}

.process-phase.active,
.process-phase.completed {
  opacity: 1;
}

.process-phase.active {
  border-color: #FF6B35;
}

.process-phase.completed {
  border-color: #1A936F;
}

.phase-header {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 16px;
  background: #FAFAFA;
  border-bottom: 1px solid #E0E0E0;
}

.process-phase.active .phase-header {
  background: #FFF5F2;
}

.process-phase.completed .phase-header {
  background: #F2FAF6;
}

.phase-num {
  font-size: 1.5rem;
  font-weight: 700;
  color: #ddd;
  line-height: 1;
}

.process-phase.active .phase-num {
  color: #FF6B35;
}

.process-phase.completed .phase-num {
  color: #1A936F;
}

.phase-info {
  flex: 1;
}

.phase-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 4px;
}

.phase-api {
  font-size: 0.75rem;
  color: #999;
  font-family: 'JetBrains Mono', monospace;
}

.phase-status {
  font-size: 0.75rem;
  padding: 4px 10px;
  background: #eee;
  color: #666;
}

.phase-status.active {
  background: #FF6B35;
  color: #fff;
}

.phase-status.completed {
  background: #1A936F;
  color: #fff;
}

/* Detalles de fase */
.phase-detail {
  padding: 16px;
}

/* Etiquetas de entidad */
.entity-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.entity-tag {
  font-size: 0.75rem;
  padding: 4px 10px;
  background: #F5F5F5;
  border: 1px solid #E0E0E0;
  color: #333;
}

/* Lista de relaciones */
.relation-list {
  font-size: 0.8rem;
}

.relation-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 0;
  border-bottom: 1px dashed #eee;
}

.relation-item:last-child {
  border-bottom: none;
}

.rel-source,
.rel-target {
  color: #333;
}

.rel-arrow {
  color: #ccc;
}

.rel-name {
  color: #FF6B35;
  font-weight: 500;
}

.relation-more {
  padding-top: 8px;
  color: #999;
  font-size: 0.75rem;
}

/* Progreso de generación de ontología */
.ontology-progress {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #FFF5F2;
  border: 1px solid #FFE0D6;
}

.progress-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #FFE0D6;
  border-top-color: #FF6B35;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.progress-text {
  font-size: 0.85rem;
  color: #333;
}

/* Estado de espera */
.waiting-state {
  padding: 16px;
  background: #F9F9F9;
  border: 1px dashed #E0E0E0;
  text-align: center;
}

.waiting-hint {
  font-size: 0.85rem;
  color: #999;
}

/* Barra de progreso */
.progress-bar {
  height: 6px;
  background: #E0E0E0;
  margin-bottom: 8px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #FF6B35;
  transition: width 0.3s;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
}

.progress-message {
  color: #666;
}

.progress-percent {
  color: #FF6B35;
  font-weight: 600;
}

/* Resultado de construcción */
.build-result {
  display: flex;
  gap: 16px;
}

.result-item {
  flex: 1;
  text-align: center;
  padding: 12px;
  background: #F5F5F5;
}

.result-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: #000;
  margin-bottom: 4px;
}

.result-label {
  font-size: 0.7rem;
  color: #999;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Botón de siguiente paso */
.next-step-section {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #E0E0E0;
}

.next-step-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px;
  background: #000;
  color: #fff;
  border: none;
  font-size: 1rem;
  font-weight: 500;
  letter-spacing: 0.05em;
  cursor: pointer;
  transition: all 0.2s;
}

.next-step-btn:hover:not(:disabled) {
  background: #FF6B35;
}

.next-step-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.btn-arrow {
  font-size: 1.2rem;
}

/* Panel de información del proyecto */
.project-panel {
  border-top: 1px solid #E0E0E0;
  background: #FAFAFA;
}

.project-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 24px;
  border-bottom: 1px solid #E0E0E0;
}

.project-icon {
  color: #FF6B35;
}

.project-title {
  font-size: 0.85rem;
  font-weight: 600;
}

.project-details {
  padding: 16px 24px;
}

.project-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 8px 0;
  border-bottom: 1px dashed #E0E0E0;
  font-size: 0.8rem;
}

.project-item:last-child {
  border-bottom: none;
}

.item-label {
  color: #999;
  flex-shrink: 0;
}

.item-value {
  color: #333;
  text-align: right;
  max-width: 60%;
  word-break: break-all;
}

.item-value.code {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: #666;
}

/* Diseño responsivo */
@media (max-width: 1024px) {
  .main-content {
    flex-direction: column;
  }
  
  .left-panel {
    width: 100% !important;
    border-right: none;
    border-bottom: 1px solid #E0E0E0;
    height: 50vh;
  }
  
  .right-panel {
    width: 100% !important;
    height: 50vh;
    opacity: 1 !important;
    transform: none !important;
  }
  
  .right-panel.hidden {
      display: none;
  }
}
</style>