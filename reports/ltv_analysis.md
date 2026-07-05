# Customer Lifetime Value (LTV) Business Analysis Report
**Prepared by**: Member 2 (Data Analyst)

---

## 1. Executive Summary
Customer Lifetime Value (LTV) is a key business metric that estimates the total revenue a business can expect from a single customer account throughout the business relationship. By analyzing LTV, our organization can make data-driven decisions on customer acquisition cost (CAC), identify high-value customer segments, and design targeted retention campaigns.

---

## 2. Methodology & Calculation
For this analysis, we define **Estimated LTV** using the formula:
$$\text{Estimated LTV} = \text{Monthly Charges} \times \text{Tenure (Months)}$$

This is a simple regression-based target suitable for cohort modeling. 
*   **Monthly Charges**: The amount billed to the customer monthly.
*   **Tenure**: The number of months the customer has stayed with the company.

*Example:* A customer paying $100/month with a tenure of 20 months has a realized LTV of $2,000.

---

## 3. LTV Segment Analysis

### A. LTV by Contract Type
Contract type is the strongest predictor of customer longevity and total value:
*   **Month-to-month**: Average LTV of **$1,370.12**
*   **One year**: Average LTV of **$3,029.83**
*   **Two year**: Average LTV of **$3,706.76**

> [!NOTE]
> Customers locked into Two-year contracts generate **2.7x more revenue** over their lifetime compared to month-to-month customers. Month-to-month contracts suffer from high churn rates early in the customer lifecycle, suppressing their average LTV.

---

### B. LTV by Payment Method
Payment methods influence customer retention convenience and billing failures:
*   **Bank transfer (automatic)**: Average LTV of **$3,077.14**
*   **Credit card (automatic)**: Average LTV of **$3,068.25**
*   **Electronic check**: Average LTV of **$2,089.68**
*   **Mailed check**: Average LTV of **$1,049.64**

> [!TIP]
> Customers utilizing **automated payment methods** (Credit Card or Bank Transfer) have almost **3x higher LTV** than those paying by mailed check. Mailed check users represent short-term, high-risk churn cohorts.

---

## 4. Key Business Recommendations
1.  **Incentivize Contract Upgrades**: Offer a one-time discount (e.g., $50 bill credit) to month-to-month customers who upgrade to 1-year or 2-year contracts. The upfront cost is heavily offset by the additional $1,600+ in expected lifetime value.
2.  **Promote Auto-Pay Options**: Implement automated enrollment prompts for bank transfers or credit cards. Since automatic payment methods show a lifetime value above $3,000, migrating mailed check or electronic check users directly extends tenure and stabilizes cash flow.

---

## 5. Presenter Speaking Script
Use this script for your team presentation to explain the LTV graphs:
*   *"Good morning/afternoon. As the Data Analyst (Member 2), I will explain our customer lifetime value analysis. We defined LTV as the product of monthly charges and tenure. Looking at the contract segments, we see that Month-to-month customers average just $1,370 in lifetime value. By comparison, Two-year contract customers generate an average of $3,706, a 2.7x increase. This proves that stabilizing tenure is key to revenue. Additionally, we found that auto-pay customers average over $3,000 in lifetime value. Based on these insights, our business strategy should aggressively prioritize upgrading month-to-month users and enrolling billing accounts in auto-pay."*
