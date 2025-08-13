"""
Test suite for Content Marketing Project Manager.
"""
import unittest
import json
from unittest.mock import Mock, patch
from pathlib import Path

from src.content_marketing_project_manager.main import validate_inputs, save_results
from src.content_marketing_project_manager.types import TaskEstimate, ProjectPlan
from src.content_marketing_project_manager.config import Config


class TestInputValidation(unittest.TestCase):
    """Test input validation functionality."""
    
    def setUp(self):
        self.valid_inputs = {
            "project_type": "Multi-Channel Content Marketing Campaign",
            "industry": "B2B SaaS",
            "project_objectives": "Drive awareness and leads",
            "project_requirements": "Blog series, email campaigns, social media",
            "team_members": "Sarah Lee (Content Strategist), Mark Johnson (SEO Writer)"
        }
    
    def test_valid_inputs(self):
        """Test that valid inputs pass validation."""
        self.assertTrue(validate_inputs(self.valid_inputs))
    
    def test_missing_required_field(self):
        """Test that missing required fields fail validation."""
        incomplete_inputs = self.valid_inputs.copy()
        del incomplete_inputs["project_type"]
        self.assertFalse(validate_inputs(incomplete_inputs))
    
    def test_empty_field(self):
        """Test that empty fields fail validation."""
        empty_inputs = self.valid_inputs.copy()
        empty_inputs["project_objectives"] = ""
        self.assertFalse(validate_inputs(empty_inputs))


class TestTypes(unittest.TestCase):
    """Test Pydantic models and type validation."""
    
    def test_task_estimate_creation(self):
        """Test TaskEstimate model creation."""
        task = TaskEstimate(
            task_name="Write Blog Post",
            format="blog",
            estimated_time_hours=5.0,
            required_resources=["writer", "editor"],
            target_publish_date="2025-09-01",
            priority="high",
            complexity="moderate"
        )
        self.assertEqual(task.task_name, "Write Blog Post")
        self.assertEqual(task.format, "blog")
        self.assertEqual(task.estimated_time_hours, 5.0)
    
    def test_invalid_date_format(self):
        """Test that invalid date formats are rejected."""
        with self.assertRaises(ValueError):
            TaskEstimate(
                task_name="Test Task",
                format="blog",
                estimated_time_hours=5.0,
                required_resources=["writer"],
                target_publish_date="invalid-date"
            )
    
    def test_project_plan_total_hours(self):
        """Test ProjectPlan total hours calculation."""
        task1 = TaskEstimate(
            task_name="Task 1",
            format="blog",
            estimated_time_hours=5.0,
            required_resources=["writer"]
        )
        task2 = TaskEstimate(
            task_name="Task 2",
            format="email",
            estimated_time_hours=3.0,
            required_resources=["writer"]
        )
        
        plan = ProjectPlan(
            tasks=[task1, task2],
            assignments=[]
        )
        
        self.assertEqual(plan.calculate_total_hours(), 8.0)


class TestConfig(unittest.TestCase):
    """Test configuration management."""
    
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    def test_config_validation_success(self):
        """Test that config validation passes with required vars."""
        config = Config()
        self.assertTrue(config.validate_config())
    
    @patch.dict('os.environ', {}, clear=True)
    def test_config_validation_failure(self):
        """Test that config validation fails without required vars."""
        config = Config()
        self.assertFalse(config.validate_config())
    
    def test_timestamp_format(self):
        """Test timestamp generation format."""
        config = Config()
        timestamp = config._get_timestamp()
        self.assertRegex(timestamp, r'\d{8}_\d{6}')


class TestSaveResults(unittest.TestCase):
    """Test result saving functionality."""
    
    def setUp(self):
        self.temp_dir = Path("/tmp/test_outputs")
        self.temp_dir.mkdir(exist_ok=True)
        
        # Mock result object
        self.mock_result = Mock()
        self.mock_result.dict.return_value = {
            "tasks": [],
            "assignments": [],
            "milestones": []
        }
    
    def test_save_results_creates_file(self):
        """Test that save_results creates output file."""
        with patch('src.content_marketing_project_manager.main.config') as mock_config:
            mock_config._get_timestamp.return_value = "20250812_120000"
            
            save_results(self.mock_result, self.temp_dir)
            
            expected_file = self.temp_dir / "content_marketing_plan_20250812_120000.json"
            self.assertTrue(expected_file.exists())
    
    def tearDown(self):
        """Clean up test files."""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete workflow."""
    
    @patch('src.content_marketing_project_manager.crew.ContentMarketingProjectManager')
    @patch('src.content_marketing_project_manager.main.config')
    def test_full_workflow_mock(self, mock_config, mock_crew_class):
        """Test full workflow with mocked dependencies."""
        # Setup mocks
        mock_config.validate_config.return_value = True
        mock_config.verbose_logging = False
        
        mock_crew_instance = Mock()
        mock_crew_result = Mock()
        mock_crew_result.dict.return_value = {"test": "data"}
        
        mock_crew_instance.kickoff.return_value = mock_crew_result
        mock_crew_class.return_value.crew.return_value = mock_crew_instance
        
        # This would test the full run() function
        # Actual implementation would depend on refactoring main.py to be more testable


if __name__ == '__main__':
    # Run specific test suites
    test_suites = [
        TestInputValidation,
        TestTypes,
        TestConfig,
        TestSaveResults,
        TestIntegration
    ]
    
    for suite_class in test_suites:
        suite = unittest.TestLoader().loadTestsFromTestCase(suite_class)
        runner = unittest.TextTestRunner(verbosity=2)
        print(f"\n=== Running {suite_class.__name__} ===")
        runner.run(suite)
