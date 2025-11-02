# file: seed_selector_int.py
import secrets
from typing import Tuple

INT32_MAX = 2_147_483_647


class SeedSelectorInt:
    """
    Seed Selector (INT) - Fixed version with previous seed tracking and value display

    Properly handles ComfyUI's control_after_generate to avoid one-run delay
    Now tracks the previous seed value and displays both values on the node
    """

    CATEGORY = "utilities/seed"
    FUNCTION = "select"

    # Class variable to store previous seeds for each node instance
    _previous_seeds = {}

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": INT32_MAX,
                    "step": 1,
                    "control_after_generate": True,
                    "display": "number"  # Display the value
                }),
            },
            "optional": {
                "max_val": ("INT", {
                    "default": INT32_MAX,
                    "min": 1,
                    "max": INT32_MAX,
                    "step": 1
                }),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("seed", "previous_seed")
    OUTPUT_NODE = False

    @classmethod
    def IS_CHANGED(cls, seed: int, **kwargs):
        # Always force execution - this prevents caching
        return float("nan")

    def _randint_inclusive(self, max_val: int) -> int:
        max_val = int(max(0, min(max_val, INT32_MAX)))
        return secrets.randbelow(max_val + 1) if max_val < INT32_MAX else secrets.randbelow(INT32_MAX)

    def select(
        self,
        seed: int,
        max_val: int = INT32_MAX,
        unique_id=None,
        extra_pnginfo=None,
    ) -> Tuple[int, int]:
        # Get the previous seed for this node instance (default to 0 for first run)
        previous_seed = self._previous_seeds.get(unique_id, 0)

        # Store current seed as the previous seed for next execution
        if unique_id is not None:
            self._previous_seeds[unique_id] = int(seed)

        # Return current seed and previous seed
        return {
            "ui": {
                "seed": [int(seed)],
                "previous_seed": [previous_seed]
            },
            "result": (int(seed), previous_seed)
        }


class MySeedSelectorInt:
    """
    My Seed Selector (INT) - Enhanced Fixed Version with previous seed tracking and display

    This version includes multiple outputs for debugging and ensures
    the seed value is passed immediately without delay.
    Now tracks the previous seed value and displays values on the node.
    """

    CATEGORY = "utilities/seed"
    FUNCTION = "select"
    OUTPUT_NODE = False

    # Class variable to store previous seeds for each node instance
    _previous_seeds = {}

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": INT32_MAX,
                    "step": 1,
                    "control_after_generate": True,
                    "display": "number"
                }),
            },
            "optional": {
                "control_after_generate": (["fixed", "increment", "decrement", "randomize"], {
                    "default": "randomize"
                }),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            }
        }

    RETURN_TYPES = ("INT", "INT", "STRING")
    RETURN_NAMES = ("seed", "previous_seed", "debug")

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # Always recompute to prevent any caching
        return float("nan")

    def select(
        self,
        seed: int,
        control_after_generate: str = "randomize",
        unique_id=None,
        extra_pnginfo=None,
    ) -> dict:
        """
        Forward the seed immediately with debug output and track previous seed
        """
        # Get the previous seed for this node instance (default to 0 for first run)
        previous_seed = self._previous_seeds.get(unique_id, 0)

        # Store current seed as the previous seed for next execution
        if unique_id is not None:
            self._previous_seeds[unique_id] = int(seed)

        s = int(seed)
        debug_msg = f"seed={s} | previous={previous_seed} | mode={control_after_generate}"

        # Return with UI display for the values
        return {
            "ui": {
                "seed_value": [s],
                "previous_seed_value": [previous_seed],
                "text": [debug_msg]
            },
            "result": (s, previous_seed, debug_msg)
        }


class SeedSelectorIntWithDisplay:
    """
    Seed Selector (INT) with Display - Alternative version with visible value labels

    This version uses a different approach to show the values directly on the node
    by including display-only text outputs that show the current values.
    """

    CATEGORY = "utilities/seed"
    FUNCTION = "select"

    # Class variable to store previous seeds for each node instance
    _previous_seeds = {}

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": INT32_MAX,
                    "step": 1,
                    "control_after_generate": True,
                    "display": "number"
                }),
            },
            "optional": {
                "max_val": ("INT", {
                    "default": INT32_MAX,
                    "min": 1,
                    "max": INT32_MAX,
                    "step": 1
                }),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            }
        }

    RETURN_TYPES = ("INT", "INT", "STRING", "STRING")
    RETURN_NAMES = ("seed", "previous_seed",
                    "seed_display", "previous_display")
    OUTPUT_NODE = False

    @classmethod
    def IS_CHANGED(cls, seed: int, **kwargs):
        return float("nan")

    def select(
        self,
        seed: int,
        max_val: int = INT32_MAX,
        unique_id=None,
        extra_pnginfo=None,
    ) -> Tuple[int, int, str, str]:
        # Get the previous seed for this node instance
        previous_seed = self._previous_seeds.get(unique_id, 0)

        # Store current seed as the previous seed for next execution
        if unique_id is not None:
            self._previous_seeds[unique_id] = int(seed)

        s = int(seed)

        # Create display strings
        seed_display = f"Current: {s}"
        previous_display = f"Previous: {previous_seed}"

        # Return all values including display strings
        return (s, previous_seed, seed_display, previous_display)


# ComfyUI registration
NODE_CLASS_MAPPINGS = {
    "SeedSelectorInt": SeedSelectorInt,
    "MySeedSelectorInt": MySeedSelectorInt,
    "SeedSelectorIntWithDisplay": SeedSelectorIntWithDisplay,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SeedSelectorInt": "Seed Selector (INT)",
    "MySeedSelectorInt": "My Seed Selector (INT)",
    "SeedSelectorIntWithDisplay": "Seed Selector with Display",
}
