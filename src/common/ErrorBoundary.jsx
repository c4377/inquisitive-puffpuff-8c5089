import React from 'react';

// Shows the actual error on screen instead of a silent white screen, so
// problems can be reported and fixed precisely.
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { error: null };
  }
  static getDerivedStateFromError(error) {
    return { error };
  }
  componentDidCatch(error, info) {
    console.error('App error:', error, info);
  }
  render() {
    if (this.state.error) {
      return (
        <div style={{ padding: 24, fontFamily: 'system-ui, sans-serif' }}>
          <h2 style={{ fontSize: 18, fontWeight: 700, marginBottom: 8 }}>Da ist etwas schiefgelaufen</h2>
          <p style={{ fontSize: 13, color: '#555', marginBottom: 12 }}>
            Bitte mach einen Screenshot von dieser Meldung — damit lässt sich der Fehler exakt beheben.
          </p>
          <pre style={{ fontSize: 11, background: '#f6f6f6', padding: 12, borderRadius: 8, whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
            {String(this.state.error?.message || this.state.error)}
            {'\n\n'}
            {String(this.state.error?.stack || '').split('\n').slice(0, 6).join('\n')}
          </pre>
          <button onClick={() => { this.setState({ error: null }); window.location.hash = '#/'; }}
            style={{ marginTop: 12, padding: '10px 16px', borderRadius: 8, background: '#7c3aed', color: '#fff', fontWeight: 700, fontSize: 13, border: 'none' }}>
            Zur Startseite
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

export default ErrorBoundary;
