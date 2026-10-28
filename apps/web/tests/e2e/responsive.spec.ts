import { test, expect } from "@playwright/test";

test.describe("Nagpur Krishi Data - Responsive & Accessibility Verification", () => {
  test.beforeEach(async ({ page }) => {
    // Intercept and mock or verify against API
    await page.goto("/");
  });

  test("should render the brand header and default Marathi language", async ({ page }) => {
    const title = page.locator("header h1");
    await expect(title).toBeVisible();
    await expect(title).toContainText("नागपूर शेती आकडे");

    // Check official drought badge
    const badge = page.locator("header").getByText(/दुष्काळग्रस्त|Drought/);
    await expect(badge).toBeVisible();
  });

  test("should switch languages seamlessly between Marathi and English", async ({ page }) => {
    // Click English switch button
    const enButton = page.getByRole("button", { name: "EN" });
    await expect(enButton).toBeVisible();
    await enButton.click();

    // Verify English brand title
    const title = page.locator("header h1");
    await expect(title).toContainText("Nagpur Krishi Data");

    // Click Marathi switch button
    const mrButton = page.getByRole("button", { name: "मराठी" });
    await expect(mrButton).toBeVisible();
    await mrButton.click();

    await expect(title).toContainText("नागपूर शेती आकडे");
  });

  test("should toggle high contrast mode", async ({ page }) => {
    const contrastBtn = page.getByTitle(/कॉन्ट्रास्ट|Contrast/i);
    await expect(contrastBtn).toBeVisible();
    await contrastBtn.click();

    // Check data-theme attribute on <html>
    const html = page.locator("html");
    await expect(html).toHaveAttribute("data-theme", "high-contrast");
  });

  test("should navigate bottom tabs (Home, Map, Crops, Market, Insights)", async ({ page }) => {
    const nav = page.locator("nav[role='navigation']");
    await expect(nav).toBeVisible();

    // Navigate to Market
    const marketTab = nav.getByText(/बाजारभाव|Market/);
    await marketTab.click();
    await expect(page.getByText(/नागपूर कृषी उत्पन्न बाजार समित्या|Nagpur Mandi Market Prices/)).toBeVisible();

    // Navigate to Map
    const mapTab = nav.getByText(/नकाशा|Map/);
    await mapTab.click();
    await expect(page.getByText(/नागपूर जिल्हा तालुका नकाशा|Nagpur Tehsil Map/)).toBeVisible();

    // Navigate back to Insights
    const insightsTab = nav.getByText(/अधिक|Insights/);
    await insightsTab.click();
    await expect(page.locator("#district-overview")).toBeVisible();
  });

  test("should verify Analysis Lab CSV download button presence", async ({ page, isMobile }) => {
    if (!isMobile) {
      const csvBtn = page.getByRole("button", { name: /CSV.*डाउनलोड|Download.*CSV/i });
      await expect(csvBtn).toBeVisible();
    }
  });
});

