"""
Unit tests for ap_common.progress module.
"""

import pytest
from unittest.mock import patch, MagicMock
from ap_common.progress import progress_iter, ProgressTracker


class TestProgressIter:
    """Tests for progress_iter function."""

    def test_returns_items_when_enabled(self):
        """Test that progress_iter yields all items when enabled."""
        items = [1, 2, 3, 4, 5]
        result = list(progress_iter(items, enabled=True))
        assert result == items

    def test_returns_items_when_disabled(self):
        """Test that progress_iter yields all items when disabled."""
        items = [1, 2, 3, 4, 5]
        result = list(progress_iter(items, enabled=False))
        assert result == items

    def test_disabled_returns_original_iterable(self):
        """Test that disabled progress_iter returns the original iterable unchanged."""
        items = [1, 2, 3]
        result = progress_iter(items, enabled=False)
        # When disabled, should return the exact same object
        assert result is items

    def test_works_with_generator(self):
        """Test that progress_iter works with generators."""

        def gen():
            yield 1
            yield 2
            yield 3

        result = list(progress_iter(gen(), enabled=True))
        assert result == [1, 2, 3]

    def test_custom_description(self):
        """Test that custom description is passed to tqdm."""
        items = [1, 2, 3]
        with patch("ap_common.progress.tqdm") as mock_tqdm:
            mock_tqdm.return_value = iter(items)
            list(progress_iter(items, desc="Custom desc", enabled=True))
            mock_tqdm.assert_called_once()
            call_kwargs = mock_tqdm.call_args
            assert call_kwargs[1]["desc"] == "Custom desc"

    def test_custom_unit(self):
        """Test that custom unit is passed to tqdm."""
        items = [1, 2, 3]
        with patch("ap_common.progress.tqdm") as mock_tqdm:
            mock_tqdm.return_value = iter(items)
            list(progress_iter(items, unit="items", enabled=True))
            mock_tqdm.assert_called_once()
            call_kwargs = mock_tqdm.call_args
            assert call_kwargs[1]["unit"] == "items"

    def test_empty_iterable(self):
        """Test that progress_iter handles empty iterables."""
        result = list(progress_iter([], enabled=True))
        assert result == []


class TestProgressTracker:
    """Tests for ProgressTracker class."""

    def test_context_manager_yields_items(self):
        """Test that ProgressTracker as context manager yields all items."""
        items = [1, 2, 3, 4, 5]
        result = []
        with ProgressTracker(items, enabled=True) as tracker:
            for item in tracker:
                result.append(item)
        assert result == items

    def test_context_manager_disabled(self):
        """Test that ProgressTracker works when disabled."""
        items = [1, 2, 3]
        result = []
        with ProgressTracker(items, enabled=False) as tracker:
            for item in tracker:
                result.append(item)
        assert result == items

    def test_set_status_when_enabled(self):
        """Test that set_status works when enabled."""
        items = [1, 2, 3]
        with patch("ap_common.progress.tqdm") as mock_tqdm:
            mock_pbar = MagicMock()
            mock_pbar.__iter__ = MagicMock(return_value=iter(items))
            mock_tqdm.return_value = mock_pbar

            with ProgressTracker(items, enabled=True) as tracker:
                for item in tracker:
                    tracker.set_status(f"Processing {item}")

            # Verify set_postfix_str was called
            assert mock_pbar.set_postfix_str.call_count == 3

    def test_set_status_when_disabled(self):
        """Test that set_status is a no-op when disabled."""
        items = [1, 2, 3]
        with ProgressTracker(items, enabled=False) as tracker:
            for item in tracker:
                # This should not raise any errors
                tracker.set_status(f"Processing {item}")

    def test_set_description_when_enabled(self):
        """Test that set_description works when enabled."""
        items = [1, 2, 3]
        with patch("ap_common.progress.tqdm") as mock_tqdm:
            mock_pbar = MagicMock()
            mock_pbar.__iter__ = MagicMock(return_value=iter(items))
            mock_tqdm.return_value = mock_pbar

            with ProgressTracker(items, enabled=True) as tracker:
                tracker.set_description("New description")
                for _ in tracker:
                    pass

            mock_pbar.set_description.assert_called_with("New description")

    def test_manual_mode_start_finish(self):
        """Test manual mode with start() and finish()."""
        tracker = ProgressTracker(desc="Manual test", enabled=True)

        with patch("ap_common.progress.tqdm") as mock_tqdm:
            mock_pbar = MagicMock()
            mock_tqdm.return_value = mock_pbar

            tracker.start()
            mock_tqdm.assert_called_once()

            tracker.update(status="Item 1")
            mock_pbar.update.assert_called()
            mock_pbar.set_postfix_str.assert_called_with("Item 1")

            tracker.finish()
            mock_pbar.close.assert_called_once()

    def test_manual_mode_disabled(self):
        """Test that manual mode works when disabled."""
        tracker = ProgressTracker(desc="Manual test", enabled=False)
        # These should all be no-ops and not raise errors
        tracker.start()
        tracker.update(status="test")
        tracker.set_status("test")
        tracker.set_description("test")
        tracker.finish()

    def test_iteration_without_context_manager(self):
        """Test that ProgressTracker can be iterated without context manager."""
        items = [1, 2, 3]
        tracker = ProgressTracker(items, enabled=False)
        result = list(tracker)
        assert result == items

    def test_empty_iterable(self):
        """Test that ProgressTracker handles empty iterables."""
        result = []
        with ProgressTracker([], enabled=True) as tracker:
            for item in tracker:
                result.append(item)
        assert result == []

    def test_none_iterable_in_manual_mode(self):
        """Test that ProgressTracker works with None iterable in manual mode."""
        tracker = ProgressTracker(desc="Manual", enabled=False)
        result = list(tracker)
        assert result == []


class TestProgressTrackerDescWidth:
    """Tests for ProgressTracker description width feature."""

    def setup_method(self):
        """Reset class default before each test."""
        ProgressTracker.set_default_desc_width(None)

    def teardown_method(self):
        """Clean up class default after each test."""
        ProgressTracker.set_default_desc_width(None)

    def test_set_default_desc_width(self):
        """Test that class default can be set."""
        ProgressTracker.set_default_desc_width(20)
        assert ProgressTracker._default_desc_width == 20

    def test_clear_default_desc_width(self):
        """Test that class default can be cleared."""
        ProgressTracker.set_default_desc_width(20)
        ProgressTracker.set_default_desc_width(None)
        assert ProgressTracker._default_desc_width is None

    def test_desc_width_pads_description(self):
        """Test that desc_width pads description with spaces."""
        tracker = ProgressTracker(desc="Short", enabled=False, desc_width=20)
        assert tracker.desc == "Short               "
        assert len(tracker.desc) == 20

    def test_desc_width_no_truncation(self):
        """Test that desc_width doesn't truncate longer descriptions."""
        tracker = ProgressTracker(
            desc="Very long description", enabled=False, desc_width=10
        )
        # ljust() doesn't truncate, just returns original if longer
        assert tracker.desc == "Very long description"

    def test_default_desc_width_applies(self):
        """Test that class default is used when no instance width provided."""
        ProgressTracker.set_default_desc_width(20)
        tracker = ProgressTracker(desc="Test", enabled=False)
        assert tracker.desc == "Test                "
        assert len(tracker.desc) == 20

    def test_instance_width_overrides_default(self):
        """Test that instance desc_width overrides class default."""
        ProgressTracker.set_default_desc_width(20)
        tracker = ProgressTracker(desc="Test", enabled=False, desc_width=15)
        assert tracker.desc == "Test           "
        assert len(tracker.desc) == 15

    def test_no_padding_without_width(self):
        """Test that no padding occurs when width is not set."""
        tracker = ProgressTracker(desc="Test", enabled=False)
        assert tracker.desc == "Test"

    def test_aligned_descriptions_with_default_width(self):
        """Test that multiple trackers with default width are aligned."""
        ProgressTracker.set_default_desc_width(20)

        tracker1 = ProgressTracker(desc="Short", enabled=False)
        tracker2 = ProgressTracker(desc="Medium length", enabled=False)
        tracker3 = ProgressTracker(desc="Very long description", enabled=False)

        # First two should be padded to 20 chars
        assert len(tracker1.desc) == 20
        assert len(tracker2.desc) == 20
        # Third is longer than 20, so stays as-is
        assert tracker3.desc == "Very long description"

    def test_desc_width_with_tqdm(self):
        """Test that padded description is passed to tqdm."""
        with patch("ap_common.progress.tqdm") as mock_tqdm:
            mock_pbar = MagicMock()
            mock_tqdm.return_value = mock_pbar

            tracker = ProgressTracker(desc="Test", enabled=True, desc_width=20)
            tracker.start()

            mock_tqdm.assert_called_once()
            call_kwargs = mock_tqdm.call_args[1]
            assert call_kwargs["desc"] == "Test                "
            assert len(call_kwargs["desc"]) == 20


class TestProgressIntegration:
    """Integration tests for progress utilities."""

    def test_progress_iter_with_file_list(self):
        """Test progress_iter with a simulated file list."""
        files = ["/path/to/file1.fits", "/path/to/file2.fits", "/path/to/file3.fits"]
        processed = []

        for f in progress_iter(files, desc="Processing files", enabled=False):
            processed.append(f)

        assert processed == files

    def test_progress_tracker_with_dynamic_status(self):
        """Test ProgressTracker with dynamic status updates."""
        files = ["file1.fits", "file2.fits", "file3.fits"]
        processed = []

        with ProgressTracker(files, desc="Processing", enabled=False) as tracker:
            for f in tracker:
                tracker.set_status(f)
                processed.append(f)

        assert processed == files
