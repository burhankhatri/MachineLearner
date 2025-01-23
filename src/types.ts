export interface Framework {
  id: 'tensorflow' | 'pytorch' | 'sklearn'
  name: string
  description: string
}

export interface Metrics {
  accuracy: string | number
  loss: string | number
}

export interface TrainingProgress {
  epoch: number
  loss: number
  accuracy: number
}

export interface ModelConfig {
  framework: Framework['id']
  hyperparameters: Record<string, any>
  architecture: string
} 