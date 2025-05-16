#!/usr/bin/env python3
"""
Test cases for Nova Sonic smoke test.

This module defines the test cases for the smoke test, allowing us to expand
our testing capabilities in the future.
"""

TEST_CASES = {
    "basic_interaction": {
        "name": "Basic End-to-End Interaction",
        "description": "Verify basic end-to-end flow with Nova Sonic.",
        "audio_file": "hello_nova.wav",
        "system_prompt": "You are a helpful assistant.",
        "expected_results": {
            "transcription_received": True,
            "audio_received": True,
            "completion_received": True
        }
    },
    
    "session_lifecycle": {
        "name": "Session Lifecycle Verification",
        "description": "Verify correct handling of session lifecycle events.",
        "audio_file": "hello_nova.wav",
        "system_prompt": "You are a helpful assistant.",
        "expected_results": {
            "session_start_ok": True,
            "prompt_start_ok": True,
            "content_start_ok": True,
            "prompt_end_ok": True,
            "session_end_ok": True
        }
    },
    
    "system_prompt": {
        "name": "Minimal System Prompt Interaction",
        "description": "Verify minimal system prompt handling.",
        "audio_file": "hello_nova.wav",
        "system_prompt": "Keep your responses concise.",
        "expected_results": {
            "transcription_received": True,
            "audio_received": True
        }
    }
}

# Default test case to run if none specified
DEFAULT_TEST_CASE = "basic_interaction" 