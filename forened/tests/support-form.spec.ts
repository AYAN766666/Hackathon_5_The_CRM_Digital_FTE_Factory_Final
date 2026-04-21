/**
 * E2E Tests for Customer Support Portal
 * Tests web form submission and ticket status checking
 */
import { test, expect } from '@playwright/test';

test.describe('Customer Support Portal', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test.describe('Support Form', () => {
    test('should display the support form with all required fields', async ({ page }) => {
      // Check form is visible
      await expect(page.getByText('Customer Support')).toBeVisible();
      await expect(page.getByLabel('Name')).toBeVisible();
      await expect(page.getByLabel('Email')).toBeVisible();
      await expect(page.getByLabel('Category')).toBeVisible();
      await expect(page.getByLabel('Message')).toBeVisible();
    });

    test('should submit a valid support request', async ({ page }) => {
      // Fill form
      await page.getByLabel('Name').fill('John Doe');
      await page.getByLabel('Email').fill('john@example.com');
      await page.getByLabel('Category').selectOption('Technical');
      await page.getByLabel('Message').fill('I am having trouble logging into my account. Can you please help me reset my password?');
      
      // Submit form
      await page.getByRole('button', { name: 'Submit Request' }).click();
      
      // Wait for success message
      await expect(page.getByText('Your support request has been received')).toBeVisible({ timeout: 10000 });
      
      // Check ticket ID is displayed
      await expect(page.getByText(/Ticket ID:/)).toBeVisible();
    });

    test('should show validation errors for invalid form', async ({ page }) => {
      // Try to submit empty form
      await page.getByRole('button', { name: 'Submit Request' }).click();
      
      // Check validation errors
      await expect(page.getByText('Name is required')).toBeVisible();
      await expect(page.getByText('Email is required')).toBeVisible();
      await expect(page.getByText('Message is required')).toBeVisible();
    });

    test('should validate email format', async ({ page }) => {
      await page.getByLabel('Name').fill('John');
      await page.getByLabel('Email').fill('invalid-email');
      await page.getByLabel('Message').fill('This is a test message with enough characters');
      
      await page.getByRole('button', { name: 'Submit Request' }).click();
      
      await expect(page.getByText('valid email')).toBeVisible();
    });

    test('should validate message length', async ({ page }) => {
      await page.getByLabel('Name').fill('John');
      await page.getByLabel('Email').fill('john@example.com');
      await page.getByLabel('Message').fill('Short');
      
      await page.getByRole('button', { name: 'Submit Request' }).click();
      
      await expect(page.getByText(/between 20 and 1000/)).toBeVisible();
    });

    test('should reset form when clicking reset button', async ({ page }) => {
      // Fill form
      await page.getByLabel('Name').fill('John Doe');
      await page.getByLabel('Email').fill('john@example.com');
      await page.getByLabel('Category').selectOption('Technical');
      await page.getByLabel('Message').fill('Test message');
      
      // Click reset
      await page.getByRole('button', { name: 'Reset' }).click();
      
      // Check form is empty
      await expect(page.getByLabel('Name')).toHaveValue('');
      await expect(page.getByLabel('Email')).toHaveValue('');
      await expect(page.getByLabel('Message')).toHaveValue('');
    });
  });

  test.describe('Ticket Status Modal', () => {
    test('should open modal when clicking status button', async ({ page }) => {
      await page.getByRole('button', { name: 'Check Ticket Status' }).click();
      
      await expect(page.getByText('Ticket Status')).toBeVisible();
      await expect(page.getByPlaceholder('e.g., ABC12345')).toBeVisible();
    });

    test('should show error for invalid ticket ID', async ({ page }) => {
      await page.getByRole('button', { name: 'Check Ticket Status' }).click();
      
      await page.getByPlaceholder('e.g., ABC12345').fill('INVALID');
      await page.getByRole('button', { name: 'Check Status' }).click();
      
      // Should show error (ticket not found or backend unavailable)
      await expect(page.getByText(/not found|unavailable/)).toBeVisible({ timeout: 10000 });
    });

    test('should close modal when clicking close button', async ({ page }) => {
      await page.getByRole('button', { name: 'Check Ticket Status' }).click();
      await page.getByRole('button', { name: 'Close' }).click();
      
      await expect(page.getByText('Ticket Status')).not.toBeVisible();
    });
  });

  test.describe('Responsive Design', () => {
    test('should work on mobile viewport', async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 667 });
      
      await expect(page.getByText('Customer Support Portal')).toBeVisible();
      await expect(page.getByLabel('Name')).toBeVisible();
    });

    test('should work on tablet viewport', async ({ page }) => {
      await page.setViewportSize({ width: 768, height: 1024 });
      
      await expect(page.getByText('Customer Support Portal')).toBeVisible();
    });
  });
});
