import { useState } from 'react'
import client from '../api/client'

const initialConfig = {
  slack_webhook: '',
  telegram_bot_token: '',
  telegram_chat_id: ''
}

export default function ConfigureAlerts() {
  const [alertConfig, setAlertConfig] = useState(initialConfig)
  const [message, setMessage] = useState('')
  const [isSuccess, setIsSuccess] = useState(false)
  const [loading, setLoading] = useState(false)
  const [testing, setTesting] = useState(false)

  const update = (key, value) => {
    setAlertConfig((c) => ({ ...c, [key]: value }))
  }

  const handleSave = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')
    try {
      await client.post('/api/configure_alerts', alertConfig)
      setMessage('Settings saved!')
      setIsSuccess(true)
    } catch (err) {
      if (err.response?.data?.message) {
        setMessage(err.response.data.message)
      } else if (typeof err.response?.data === 'string' && err.response.data.trim()) {
        setMessage(err.response.data)
      } else if (err.message) {
        setMessage(err.message)
      } else {
        setMessage('Error saving settings')
      }
      setIsSuccess(false)
    }
    setLoading(false)
  }

  const handleTest = async () => {
    setTesting(true)
    setMessage('')
    try {
      const { data } = await client.post('/api/test_alerts')
      const resultMessages = Object.entries(data.results || {})
        .map(([channel, result]) => `${channel}: ${result.message}`)
        .join(' | ')
      setMessage(resultMessages || data.message || 'Test alert processed.')
      setIsSuccess(Object.values(data.results || {}).some((result) => result.success))
    } catch (err) {
      if (err.response?.data?.message) {
        setMessage(err.response.data.message)
      } else if (typeof err.response?.data === 'string' && err.response.data.trim()) {
        setMessage(err.response.data)
      } else if (err.message) {
        setMessage(err.message)
      } else {
        setMessage('Error testing alerts')
      }
      setIsSuccess(false)
    }
    setTesting(false)
  }

  return (
    <div className="card">
      <h2 className="section-title">Configure Alerts</h2>
      <form onSubmit={handleSave}>
        <div className="form-group">
          <label className="label" htmlFor="slack-webhook">Slack Webhook URL</label>
          <input
            id="slack-webhook"
            type="url"
            value={alertConfig.slack_webhook}
            onChange={(e) => update('slack_webhook', e.target.value)}
            placeholder="https://hooks.slack.com/..."
          />
        </div>
        <div className="form-group">
          <label className="label" htmlFor="telegram-token">Telegram Bot Token</label>
          <input
            id="telegram-token"
            type="text"
            value={alertConfig.telegram_bot_token}
            onChange={(e) => update('telegram_bot_token', e.target.value)}
            placeholder="Bot token"
          />
        </div>
        <div className="form-group">
          <label className="label" htmlFor="telegram-chat">Telegram Chat ID</label>
          <input
            id="telegram-chat"
            type="text"
            value={alertConfig.telegram_chat_id}
            onChange={(e) => update('telegram_chat_id', e.target.value)}
            placeholder="Chat ID"
          />
        </div>
        <div className="action-row">
          <button type="submit" disabled={loading}>
            {loading ? 'Saving...' : 'Save Settings'}
          </button>
          <button
            type="button"
            className="warning"
            onClick={handleTest}
            disabled={testing}
          >
            {testing ? 'Testing...' : 'Send Test Alert'}
          </button>
        </div>
        {message && (
          <div className={`alert ${isSuccess ? 'success' : 'error'}`}>{message}</div>
        )}
      </form>

      <style>{`
        .section-title { margin: 0 0 1rem; font-size: 1.1rem; font-weight: 600; }
        .form-group { margin-bottom: 1rem; }
        .action-row {
          display: flex;
          gap: 0.75rem;
          flex-wrap: wrap;
          margin-top: 0.25rem;
        }
        .action-row button {
          flex: 1 1 180px;
        }
      `}</style>
    </div>
  )
}
