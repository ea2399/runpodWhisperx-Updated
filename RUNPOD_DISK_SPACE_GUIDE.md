# 💾 RunPod Disk Space Guide ("No space left on device")

## 🎯 The Problem

When you see the error `Error: ... No space left on device (os error 28)`, it means the RunPod worker running your job doesn't have enough disk space to download the large Whisper model you requested (especially `large-v2` or `large-v3`).

- **The `large-v3` model is ~3 GB.**
- Default serverless workers often have limited storage.

## 🔧 The Solution: Increase Worker Disk Space

You need to edit your RunPod endpoint to allocate more storage to each worker.

### Step-by-Step Instructions:

1.  **Navigate to Your Endpoints**
    - Go to the [RunPod Console](https://runpod.io/console/serverless/user/endpoints).
    - Or navigate via **Serverless > My Endpoints**.

2.  **Edit Your Endpoint**
    - Find the endpoint you're using for WhisperX.
    - Click the **three dots (...)** on the right side.
    - Select **Edit Endpoint** from the dropdown menu.

    ![Edit Endpoint Menu](https://i.imgur.com/example-image.png) <!-- Placeholder image -->

3.  **Increase Storage Allocation**
    - In the endpoint settings, find the **Volume Size** or **Temporary Storage** field.
    - **Increase the value.**

    **Recommended Sizes:**
    - For `large-v2` model: **10 GB**
    - For `large-v3` model: **15 GB** (This is a safe value)

    ![Storage Setting](https://i.imgur.com/example-image.png) <!-- Placeholder image -->

4.  **Update the Endpoint**
    - Scroll down and click **Update Endpoint**.

## ✅ What Happens Next?

- Your endpoint will update.
- **Any new job** you run will be assigned to a new worker that has the larger disk space you allocated.
- The "No space left on device" error will be resolved.

## 💡 Pro Tip

- **Don't set it too low**: It's better to have a little extra space than to hit the limit again. 15 GB is a very safe bet for the largest models.
- **Cost**: Be aware that increasing volume size may slightly increase the cost of your serverless runs, but it's usually a very small amount.

By following these steps, you provide enough space for the powerful `large-v3` model to be downloaded and used for your high-quality transcriptions. 