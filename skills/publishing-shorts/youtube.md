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
   - AI use: the question asks whether AI was used in four listed ways: a real person appearing to say or do something, altered footage of a real event or place, a realistic scene that didn't occur, or music as the main focus. A synthetic narrator over a drawn animation, with a quiet bed, matches none of them, so the answer is "No, AI wasn't used".
5. Click **Next** three times (use `find` for the Next button rather than fixed coordinates, which move when the window is resized) (Video elements → Checks → Visibility). Checks should read "No issues found".
6. **Visibility → Schedule:**
   - Date: open the date dropdown, then type the date into the picker's own text field (for example `23 Nov 2026`) and press Return. Clicking a calendar cell by coordinates breaks when the window size changes.
   - Time: typing into the time field doesn't stick (16 Nov). Click the time input by its `find` ref, then `find` the option ("07:30", "19:30") in the list that opens, scroll to it and click it. Zoom in and read back the date and time.
   - Time zone: keep local.
7. Click **Schedule**. Copy the link from the "Video scheduled" dialog (`youtube.com/shorts/<id>`) and log it.

## Rescheduling and editing after upload
- **Move a scheduled video:** open its edit page → Visibility → the date picker and the time option list as above → Done → Save.
- **Save takes a few seconds.** Wait for the "Changes saved" toast before navigating away; navigating during a save is blocked by a "Leave site?" dialog.
- **Description text** can be changed in place with `javascript_tool`: replace the text node inside the description's `#textbox[contenteditable="true"]`, dispatch an `input` event, then Save.

## Clicking reliably
Prefer element refs from `find` over screen coordinates. If you do use coordinates, take a fresh screenshot after any window resize or scroll and measure again: a click at a stale position lands on the wrong control or on nothing. After a missed click, take a screenshot, read which step the dialog's stepper is on, and check the Audience and Visibility choices before you continue.

## Long-form videos (16:9, verified on L01)
1. **Upload:** the owner drags the master into Studio (browser tools cap uploads at about 10 MB). The draft appears under Content → Videos; open it with **Edit draft**. Details can be filled in while YouTube is still checking the file.
2. **Details:**
   - Title (cmd+A, type) and description, with the timestamps from `timestamps.txt`.
   - **Don't press Escape** to close the hashtag suggestions: it closes the whole dialog. It autosaves, but you have to reopen the draft.
   - Thumbnail: upload straight into the hidden `input[type=file]` in the Thumbnail section (no patch needed).
   - Audience "not made for kids", Show more → paid promotion No, AI use No (per the listed cases), category Education.
   - **Video language: English.** Without it, the Subtitles "Add" button stays disabled.
3. **Video elements → Subtitles → Add → Upload file → With timing → Continue:** patch `HTMLInputElement.prototype.click` first (as in `instagram.md`), upload the `.srt` into the file input, then **Done**. Studio confirms "English subtitles published".
4. **Visibility → Schedule:**
   - Pick the day in the date picker.
   - Click the time **input** by its `find` ref (coordinates missed it once and selected the page), cmd+A, type `19:30`, Return.
   - Don't click the Schedule heading afterwards: it collapses the section. Read back the date and time, then click **Schedule**.
   - The confirmation says "Your video will be set to public on <date> at <time>"; log the ID.

