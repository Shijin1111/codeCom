from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import Note, Subheading, CodeExecution, Problem
from datetime import datetime, timedelta

class ModelsTestCase(TestCase):

    def setUp(self):
        # Set up initial test data for Note and Subheading
        self.note = Note.objects.create(title="Test Note")
        self.subheading = Subheading.objects.create(
            note=self.note,
            heading="Test Heading",
            content="Test Content"
        )
        # Set up test data for CodeExecution
        self.code_execution = CodeExecution.objects.create(
            code="print('Hello, World!')",
            input_data="",
            output="Hello, World!"
        )
        # Set up test data for Problem
        self.problem = Problem.objects.create(
            title="Sample Problem",
            description="This is a sample problem description."
        )

    # Test Note model
    def test_note_creation(self):
        """Test that a Note is created successfully."""
        self.assertEqual(self.note.title, "Test Note")
        self.assertIsNotNone(self.note.created_at)

    # Test Subheading model
    def test_subheading_creation(self):
        """Test that a Subheading is created and linked to the correct Note."""
        self.assertEqual(self.subheading.heading, "Test Heading")
        self.assertEqual(self.subheading.note, self.note)
        self.assertEqual(self.subheading.content, "Test Content")
        self.assertEqual(str(self.subheading), "Test Note - Test Heading")

    # Test CodeExecution model
    def test_code_execution(self):
        """Test that CodeExecution saves and retrieves correctly."""
        self.assertEqual(self.code_execution.code, "print('Hello, World!')")
        self.assertEqual(self.code_execution.output, "Hello, World!")
        self.assertIsNotNone(self.code_execution.execution_time)

    # Test Problem model
    def test_problem_creation(self):
        """Test that a Problem is created successfully."""
        self.assertEqual(self.problem.title, "Sample Problem")
        self.assertEqual(self.problem.description, "This is a sample problem description.")
        self.assertIsNotNone(self.problem.created_at)
        self.assertIsNotNone(self.problem.updated_at)

    # Test relationships
    def test_note_subheading_relationship(self):
        """Test that the Note model correctly relates to its Subheadings."""
        subheadings = self.note.subheadings.all()
        self.assertEqual(subheadings.count(), 1)
        self.assertEqual(subheadings.first(), self.subheading)

    def test_problem_image_field(self):
        """Test that the img field in Problem can be blank or null."""
        # Check if the image field is None or points to an empty image
        self.assertIsNone(self.problem.img.name)  # img.name will be None if there's no file



