/**
 * Kappa Orb - Expert Assistant Page
 * Dedicated interface for Kappa Expert Engine
 */

import KappaOrbWidget from '@/components/KappaOrbWidget';

export const metadata = {
  title: 'Kappa Orb - Terra Nature Expert Assistant',
  description: 'Voice-powered expert assistant for Terra Nature projects',
};

export default function KappaOrbPage() {
  return (
    <div
      style={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '20px',
        fontFamily: 'system-ui, -apple-system, sans-serif',
      }}
    >
      {/* Background Animation */}
      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.7; }
        }

        @keyframes float {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-20px); }
        }

        body {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          background-attachment: fixed;
        }
      `}</style>

      {/* Floating Orb Animation */}
      <div
        style={{
          position: 'absolute',
          top: '10%',
          left: '5%',
          width: '120px',
          height: '120px',
          borderRadius: '50%',
          background: 'rgba(255, 255, 255, 0.1)',
          animation: 'float 6s ease-in-out infinite',
          backdropFilter: 'blur(10px)',
        }}
      />
      <div
        style={{
          position: 'absolute',
          bottom: '10%',
          right: '5%',
          width: '100px',
          height: '100px',
          borderRadius: '50%',
          background: 'rgba(255, 255, 255, 0.15)',
          animation: 'float 8s ease-in-out infinite 1s',
          backdropFilter: 'blur(10px)',
        }}
      />

      {/* Main Content */}
      <div style={{ position: 'relative', zIndex: 1, width: '100%' }}>
        {/* Page Header */}
        <div
          style={{
            textAlign: 'center',
            marginBottom: '40px',
            color: 'white',
          }}
        >
          <h1
            style={{
              fontSize: '48px',
              fontWeight: '700',
              margin: '0 0 12px 0',
              letterSpacing: '-1px',
            }}
          >
            🔮 Kappa Orb
          </h1>
          <p
            style={{
              fontSize: '18px',
              margin: 0,
              opacity: 0.9,
              fontWeight: '300',
            }}
          >
            Expert Assistant für Terra Nature
          </p>
          <p
            style={{
              fontSize: '14px',
              margin: '12px 0 0 0',
              opacity: 0.8,
            }}
          >
            Sprachgesteuert | Multi-Expert Validierung | MRV-Compliance
          </p>
        </div>

        {/* Feature Grid */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '16px',
            marginBottom: '40px',
            maxWidth: '900px',
            margin: '0 auto 40px',
          }}
        >
          {[
            { icon: '🎤', title: 'Sprachbedienung', desc: 'Natürliche Sprachabfragen' },
            { icon: '🧠', title: '9 Experten', desc: 'Multi-Perspektiven-Validierung' },
            { icon: '✅', title: 'MRV-Konform', desc: 'Regulatorische Compliance' },
            { icon: '💾', title: 'Gedächtnis', desc: 'Projekt-Gedächtnis & Memory' },
          ].map((feature, idx) => (
            <div
              key={idx}
              style={{
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                borderRadius: '8px',
                padding: '16px',
                textAlign: 'center',
                color: 'white',
              }}
            >
              <div style={{ fontSize: '32px', marginBottom: '8px' }}>{feature.icon}</div>
              <div style={{ fontWeight: '600', marginBottom: '4px', fontSize: '14px' }}>
                {feature.title}
              </div>
              <div style={{ fontSize: '12px', opacity: 0.8 }}>{feature.desc}</div>
            </div>
          ))}
        </div>

        {/* Kappa Widget */}
        <div style={{ maxWidth: '700px', margin: '0 auto' }}>
          <KappaOrbWidget embedded={false} />
        </div>
      </div>

      {/* Footer Navigation */}
      <div
        style={{
          position: 'absolute',
          bottom: '20px',
          left: '20px',
          zIndex: 1,
        }}
      >
        <a
          href="/"
          style={{
            color: 'white',
            textDecoration: 'none',
            fontSize: '14px',
            padding: '8px 16px',
            backgroundColor: 'rgba(255, 255, 255, 0.2)',
            borderRadius: '6px',
            display: 'inline-block',
            backdropFilter: 'blur(10px)',
          }}
        >
          ← Zurück zum Dashboard
        </a>
      </div>

      {/* Help Text */}
      <div
        style={{
          position: 'absolute',
          bottom: '20px',
          right: '20px',
          zIndex: 1,
          backgroundColor: 'rgba(255, 255, 255, 0.1)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.2)',
          borderRadius: '8px',
          padding: '12px 16px',
          color: 'white',
          fontSize: '12px',
          maxWidth: '250px',
        }}
      >
        <strong>💡 Tipp:</strong> Starten Sie mit einer natürlichsprachlichen Frage oder nutzen Sie
        den Validierungsmodus zur Expertenprüfung.
      </div>
    </div>
  );
}
