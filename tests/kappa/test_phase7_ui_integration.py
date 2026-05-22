"""
Tests for Phase 7: UI Integration with Kappa Orb Widget
Tests for Terra-Kappa integration and dashboard embedding
"""

import pytest
from pathlib import Path


class TestKappaUIIntegration:
    """Tests for Kappa UI integration components"""

    def test_kappa_widget_file_exists(self):
        """Test that KappaOrbWidget component exists"""
        widget_file = Path('/home/user/terra-nature-v2.4/components/KappaOrbWidget.tsx')
        assert widget_file.exists(), "KappaOrbWidget.tsx should exist"

    def test_kappa_page_file_exists(self):
        """Test that Kappa page exists"""
        page_file = Path('/home/user/terra-nature-v2.4/app/kappa-ui/page.tsx')
        assert page_file.exists(), "Kappa Orb page should exist"

    def test_use_kappa_orb_hook_file_exists(self):
        """Test that useKappaOrb hook exists"""
        hook_file = Path('/home/user/terra-nature-v2.4/app/kappa-ui/hooks/useKappaOrb.ts')
        assert hook_file.exists(), "useKappaOrb hook should exist"

    def test_dashboard_integration_file_exists(self):
        """Test that dashboard integration exists"""
        integration_file = Path(
            '/home/user/terra-nature-v2.4/lib/kappa/integration/dashboard-integration.tsx'
        )
        assert integration_file.exists(), "Dashboard integration should exist"

    def test_terra_metrics_bridge_file_exists(self):
        """Test that terra metrics bridge exists"""
        bridge_file = Path(
            '/home/user/terra-nature-v2.4/lib/kappa/integration/terra-metrics-bridge.ts'
        )
        assert bridge_file.exists(), "Terra metrics bridge should exist"

    def test_widget_content_includes_voice_control(self):
        """Test that widget includes voice control elements"""
        widget_file = Path('/home/user/terra-nature-v2.4/components/KappaOrbWidget.tsx')
        content = widget_file.read_text()

        assert 'startListening' in content
        assert 'stopListening' in content
        assert 'isListening' in content
        assert '🎤' in content

    def test_widget_content_includes_validation(self):
        """Test that widget includes validation support"""
        widget_file = Path('/home/user/terra-nature-v2.4/components/KappaOrbWidget.tsx')
        content = widget_file.read_text()

        assert 'validationResult' in content
        assert 'Validierung' in content or 'validation' in content
        assert 'Expert Mode' in content or 'Mode' in content

    def test_page_content_includes_features(self):
        """Test that page includes feature descriptions"""
        page_file = Path('/home/user/terra-nature-v2.4/app/kappa-ui/page.tsx')
        content = page_file.read_text()

        assert 'Sprachbedienung' in content or '🎤' in content
        assert 'Experten' in content
        assert 'MRV' in content or 'Compliance' in content

    def test_hook_includes_query_method(self):
        """Test that hook includes query method"""
        hook_file = Path('/home/user/terra-nature-v2.4/app/kappa-ui/hooks/useKappaOrb.ts')
        content = hook_file.read_text()

        assert 'query' in content
        assert 'startListening' in content
        assert 'validate' in content

    def test_dashboard_integration_includes_floating_widget(self):
        """Test that dashboard integration includes floating widget"""
        integration_file = Path(
            '/home/user/terra-nature-v2.4/lib/kappa/integration/dashboard-integration.tsx'
        )
        content = integration_file.read_text()

        assert 'position: fixed' in content or 'floating' in content.lower()
        assert 'KappaDashboardWidget' in content
        assert '🔮' in content


class TestPhase7Completeness:
    """Tests to verify Phase 7 implementation completeness"""

    def test_all_phase7_files_created(self):
        """Test that all required Phase 7 files are created"""
        required_files = [
            '/home/user/terra-nature-v2.4/components/KappaOrbWidget.tsx',
            '/home/user/terra-nature-v2.4/app/kappa-ui/page.tsx',
            '/home/user/terra-nature-v2.4/app/kappa-ui/hooks/useKappaOrb.ts',
            '/home/user/terra-nature-v2.4/lib/kappa/integration/terra-metrics-bridge.ts',
            '/home/user/terra-nature-v2.4/lib/kappa/integration/dashboard-integration.tsx',
        ]

        for file_path in required_files:
            path = Path(file_path)
            assert path.exists(), f"Required file {file_path} should exist"

    def test_phase7_components_are_tsx(self):
        """Test that Phase 7 components use TypeScript/TSX"""
        component_files = [
            '/home/user/terra-nature-v2.4/components/KappaOrbWidget.tsx',
            '/home/user/terra-nature-v2.4/app/kappa-ui/page.tsx',
            '/home/user/terra-nature-v2.4/lib/kappa/integration/dashboard-integration.tsx',
        ]

        for file_path in component_files:
            path = Path(file_path)
            assert path.suffix == '.tsx', f"{file_path} should be TSX"

    def test_phase7_has_proper_client_directives(self):
        """Test that client components include 'use client' directive"""
        client_components = [
            '/home/user/terra-nature-v2.4/components/KappaOrbWidget.tsx',
            '/home/user/terra-nature-v2.4/app/kappa-ui/hooks/useKappaOrb.ts',
            '/home/user/terra-nature-v2.4/lib/kappa/integration/dashboard-integration.tsx',
        ]

        for file_path in client_components:
            path = Path(file_path)
            if path.exists():
                content = path.read_text()
                if 'useState' in content or 'useEffect' in content or 'useCallback' in content:
                    assert "'use client'" in content or '"use client"' in content, \
                        f"{file_path} should have 'use client' directive"
