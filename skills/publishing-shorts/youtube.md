# YouTube Studio (browser automation)

## Channel setup (once, after the owner has created the channel)
- A second channel on the same Google account needs YouTube's "advanced features" (phone verification). That step belongs to the owner: youtube.com/verify, then youtube.com/channel_switcher → Create a channel.
- Studio → Customisation → Profile:
  - **Banner:** 2560×1440. Keep all text inside the centred 1235×338 (left 662, top 551). The crop dialog's "Viewable on all devices" box is that area, and its label chip covers the top-left corner of it.
  - **Picture:** a simple mark at 800×800. Confirm both crop dialogs with **Done**, then **Publish**.
  - **Description and links:** add the website as the first link.
- The page refuses to navigate away with unpublished changes ("Leave site?"). Wait for the "Changes published" toast first.

## Uploading and scheduling a Short
1. Go to `https://studio.youtube.com/channel/<id>/videos/upload?d=ud` and find the hidden `input[type=file]` in the dialog. Upload the file into it; don't click "Select files", which opens a native picker.
2. **Details:**
   - Title: cmd+A in the title box, then type. Phrase it as the question a viewer would search for, which the video answers ("Does a Microwave Cook Food From the Inside Out?").
   - Description: type it, then click the "Details" heading to close the hashtag suggestions.
3. **Audience:** "No, it's not made for kids".
4. **Show more:**
   - Paid promotion: No.
   - AI use: answer against the listed cases. A synthetic narrator over a drawn animation matches none of them, so the answer is "No".
5. Click **Next** three times (use `find` for the Next button rather than fixed coordinates, which move when the window is resized) (Video elements → Checks → Visibility). Checks should read "No issues found".
6. **Visibility → Schedule:**
   - Date picker: click the day.
   - Time: cmd+A in the time field, type `19:30`, press Return.
   - Time zone: keep local.
7. Click **Schedule**. Copy the link from the "Video scheduled" dialog (`youtube.com/shorts/<id>`) and log it.

## Clicking reliably
Prefer element refs from `find` over screen coordinates. If you do use coordinates, take a fresh screenshot after any window resize or scroll and measure again: a click at a stale position lands on the wrong control or on nothing. After a missed click, take a screenshot, read which step the dialog's stepper is on, and check the Audience and Visibility choices before you continue.
