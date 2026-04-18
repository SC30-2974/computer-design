<template>
  <div class="energy-core-canvas">
    <TresCanvas clear-color="#f3fff8" alpha>
      <TresPerspectiveCamera :position="[0, 0, 7]" :fov="42" />
      <TresAmbientLight :intensity="1.5" color="#ffffff" />
      <TresDirectionalLight :position="[3.2, 4.2, 4.8]" :intensity="2.1" color="#93c5fd" />
      <TresPointLight :position="[-4, -1.2, 4]" :intensity="1.35" color="#22d3ee" />
      <TresPointLight :position="[0, 4, -2]" :intensity="0.9" color="#bfdbfe" />

      <TresGroup ref="coreGroupRef">
        <TresMesh>
          <TresIcosahedronGeometry :args="[1.02, 1]" />
          <TresMeshPhysicalMaterial
            color="#e0f2fe"
            :metalness="0.2"
            :roughness="0.1"
            :transmission="0.75"
            :thickness="1.2"
            emissive="#0ea5e9"
            :emissiveIntensity="0.08"
          />
        </TresMesh>

        <TresMesh :rotation="[0.7, 0.3, 0.4]">
          <TresTorusGeometry :args="[1.52, 0.06, 32, 140]" />
          <TresMeshStandardMaterial color="#7dd3fc" emissive="#22d3ee" :emissiveIntensity="0.65" />
        </TresMesh>

        <TresMesh :rotation="[0.3, 0.5, 1.2]">
          <TresCylinderGeometry :args="[0.66, 0.66, 0.28, 6, 1, false]" />
          <TresMeshPhysicalMaterial
            color="#ffffff"
            :metalness="0.26"
            :roughness="0.14"
            :transmission="0.42"
            :thickness="0.55"
            emissive="#0ea5e9"
            :emissiveIntensity="0.26"
          />
        </TresMesh>

        <TresMesh :position="[0, 0, 0.04]">
          <TresBoxGeometry :args="[0.6, 0.6, 0.2]" />
          <TresMeshStandardMaterial color="#bae6fd" emissive="#22d3ee" :emissiveIntensity="0.2" />
        </TresMesh>
      </TresGroup>

      <TresGroup
        v-for="(orbit, orbitIndex) in orbitTracks"
        :key="`orbit-${orbitIndex}`"
        :rotation="orbit.rotation"
        :ref="(el) => setOrbitGroupRef(el, orbitIndex)"
      >
        <TresMesh
          v-for="particle in orbit.particles"
          :key="`orbit-${orbitIndex}-${particle.id}`"
          :position="particle.position"
          :scale="[particle.scale, particle.scale, particle.scale]"
        >
          <TresSphereGeometry :args="[0.06, 10, 10]" />
          <TresMeshBasicMaterial color="#7dd3fc" :transparent="true" :opacity="particle.opacity" />
        </TresMesh>
      </TresGroup>
    </TresCanvas>
  </div>
</template>

<script setup lang="ts">
import { useLoop } from '@tresjs/core'
import { onBeforeUnmount, onMounted, ref } from 'vue'
import type { Group } from 'three'

type ParticleNode = {
  id: string
  position: [number, number, number]
  scale: number
  opacity: number
}

type OrbitTrack = {
  speed: number
  rotation: [number, number, number]
  particles: ParticleNode[]
}

const coreGroupRef = ref<Group | null>(null)
const orbitGroupRefs = ref<Array<Group | null>>([])

const pointerTarget = { x: 0, y: 0 }
const pointerSmooth = { x: 0, y: 0 }

const buildOrbitParticles = (radius: number, count: number, zWave = 0.45): ParticleNode[] => {
  const nodes: ParticleNode[] = []
  for (let index = 0; index < count; index += 1) {
    const angle = (index / count) * Math.PI * 2
    const wobble = Math.sin(angle * 3.6) * zWave
    nodes.push({
      id: `${radius}-${index}`,
      position: [Math.cos(angle) * radius, wobble, Math.sin(angle) * radius],
      scale: 0.7 + ((index % 5) * 0.12),
      opacity: 0.35 + ((index % 6) * 0.09),
    })
  }
  return nodes
}

const orbitTracks: OrbitTrack[] = [
  {
    speed: 0.12,
    rotation: [0.25, 0.15, 0.38],
    particles: buildOrbitParticles(2.28, 32, 0.45),
  },
  {
    speed: -0.17,
    rotation: [1.1, 0.25, 0.1],
    particles: buildOrbitParticles(2.75, 38, 0.58),
  },
  {
    speed: 0.09,
    rotation: [0.6, 1.05, 0.32],
    particles: buildOrbitParticles(3.22, 44, 0.66),
  },
]

const setOrbitGroupRef = (el: unknown, index: number) => {
  orbitGroupRefs.value[index] = (el as Group | null) ?? null
}

const onPointerMove = (event: PointerEvent) => {
  const width = window.innerWidth || 1
  const height = window.innerHeight || 1
  pointerTarget.x = (event.clientX / width - 0.5) * 2
  pointerTarget.y = (event.clientY / height - 0.5) * 2
}

const { onRender } = useLoop()

onRender(({ elapsed }) => {
  pointerSmooth.x += (pointerTarget.x - pointerSmooth.x) * 0.06
  pointerSmooth.y += (pointerTarget.y - pointerSmooth.y) * 0.06

  if (coreGroupRef.value) {
    coreGroupRef.value.rotation.y += 0.008
    coreGroupRef.value.rotation.x = pointerSmooth.y * 0.22
    coreGroupRef.value.rotation.z = pointerSmooth.x * 0.08
    coreGroupRef.value.position.y = Math.sin(elapsed * 0.95) * 0.22
  }

  orbitTracks.forEach((orbit, index) => {
    const group = orbitGroupRefs.value[index]
    if (!group) return
    group.rotation.y += orbit.speed * 0.02
    group.rotation.x += orbit.speed * 0.012
    group.position.y = Math.sin(elapsed * (0.65 + index * 0.14)) * 0.09
  })
})

onMounted(() => {
  window.addEventListener('pointermove', onPointerMove, { passive: true })
})

onBeforeUnmount(() => {
  window.removeEventListener('pointermove', onPointerMove)
})
</script>

<style scoped>
.energy-core-canvas {
  width: 100%;
  height: 100%;
}
</style>

