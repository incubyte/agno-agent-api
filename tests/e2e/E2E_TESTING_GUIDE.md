# End-to-End Testing Guide

This guide explains how to run and maintain the end-to-end tests for the Agno Agent API.

## Prerequisites

1. A valid Anthropic API key (Claude)
2. An email account for sending test emails
3. Python environment with all dependencies installed

## Setup

1. Create a `.env.test` file with the following variables:

   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key
   SENDER_EMAIL=your_sender_email@example.com
   SENDER_PASSWORD=your_email_password
   TEST_EMAIL=your_test_receiver_email@example.com
   SKIP_EXTERNAL_CALLS=false
   ```

2. Install test dependencies:
   ```
   pip install pytest pytest-asyncio python-dotenv
   ```

## Running the Tests

### Run E2E tests from specific file

```
pytest tests/e2e/test_agent_route_e2e.py -v
```

### Run only integration tests (real API calls but mocked email)

```
pytest tests/e2e/test_agent_route_e2e.py -v -m integration
```

### Run only specific E2E tests

```
pytest tests/e2e/test_agent_route_e2e.py::test_agent_endpoint_e2e -v
```

### Skip tests that make external API calls

Update the `.env.test` file:

```
SKIP_EXTERNAL_CALLS=true
```

## CI/CD Integration

For CI/CD pipelines, you can:

1. Store the credentials as secrets in your CI/CD platform
2. Set `SKIP_EXTERNAL_CALLS=true` for quicker builds that don't rely on external services
3. Schedule full E2E tests to run periodically (e.g., nightly) with `SKIP_EXTERNAL_CALLS=false`

## Test Scenarios

The E2E tests cover:

1. Full end-to-end flow with actual API calls, PDF generation, and email sending
2. Error handling for invalid input
3. Performance characteristics
4. Integration testing with mocked components

## Extending the Tests

When adding new features:

1. Add new test cases to cover the feature's happy path
2. Add tests for error conditions and edge cases
3. Consider performance implications with a performance test
