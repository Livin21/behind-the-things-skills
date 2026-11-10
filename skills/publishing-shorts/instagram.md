# Instagram Reels (browser automation)

## Account setup (once, after the owner has signed up)
- `instagram.com/accounts/edit/`: upload the profile photo into the hidden file input, write the bio (150 characters max), Submit. The website link can only be edited in the mobile app; ask the owner.
- Switch to a professional account at `instagram.com/accounts/convert_to_professional_account/`: Creator → category (for example Education). This unlocks insights and Business Suite scheduling.
- The display name is edited in Meta Accounts Center, not on the edit page.

## Posting now (web)
Create → Post → upload into the hidden file input.
1. Crop: the icon at the bottom-left → **Original**. The default is a 1:1 crop.
2. Edit: Cover photo → upload your cover into its hidden file input.
3. Caption, then **Share**. Video posts are shared as Reels.

## Scheduling (web can't, so use Meta Business Suite)
1. The owner opens business.facebook.com and signs in **with Instagram** if their Facebook account doesn't manage this profile. Their session may open in a new tab, so re-read the open tabs.
2. Go to `business.facebook.com/latest/reels_composer?asset_id=<id>&business_id=<id>` (the IDs are in the URL after login).
3. **Add video opens a native file picker.** Before clicking it, run:
   ```js
   const orig = HTMLInputElement.prototype.click;
   HTMLInputElement.prototype.click = function () {
     if (this.type === 'file') { this.style.display = 'block';
       if (!document.body.contains(this)) document.body.appendChild(this); return; }
     return orig.call(this);
   };
   ```
   Then click **Add video**, find the file input now at the bottom of the page, and upload into it. Re-run the patch after every page navigation.
4. **Caption.** The hashtag autocomplete merges tags if you type `#tag` directly (`#learnsometh#MicrowaveOven`), and also when you go too fast. Instead:
   - Keep the tag list from the copy you wrote (step 3 of SKILL.md); the repair below needs it. Type the whole caption with the tags as plain words on the last line: `howitworks science smokedetector explained physics learnsomethingnew`.
   - Escape, then cmd+Left (to the start of that line), type `#`, wait 1 s, Escape.
   - For each next tag: alt+Right, Right (to the start of the next word), type `#`, wait 1 s, Escape.
   - Zoom in on the box. If two tags merged: cmd+Right to the end of the line, Backspace back to just after the last good tag and its space (select-all + Delete doesn't work in this box), type the remaining tags from your list as plain words, Escape, alt+Left once per retyped word to reach the first of them, then `#`, wait, Escape and alt+Right, Right as above. Zoom in again.
   - Click outside the box.
5. **Thumbnail.** Choose suggested: pick the frame showing the hook caption. If none shows it: re-run the patch if the page has navigated, click Upload image → the "Upload Image" link, then upload the episode's cover into the new `image/*` file input at the bottom of the page.
   Before moving on, the preview panel should say "Your reel is safe to publish" (Meta's copyright check on the video).
6. Next (Edit: no audio) → Next (Share) → **Schedule** (the option under "Scheduling options"):
   - Date: click the date box, cmd+A, type `dd/mm/yyyy` (for example `23/11/2026`), Return.
   - Time: click the hours spinbutton and type `19`, then the minutes spinbutton and type `30`.
   - Zoom in and read back the date and time. The date shows the month as a word ("23 November 2026", "2 December 2026"); if the month is wrong, the field took the date as mm/dd, so retype it that way. The time must read the release slot from `CHANNEL.md` (for example "19:30").
7. Check the caption is final **before** scheduling: Business Suite's "Edit Reel" on an already-scheduled Reel accepts a caption change and keeps the schedule, but saves the old caption (tested on six Reels). To change one later, edit the caption on instagram.com after it goes live, or delete and re-create the scheduled Reel (ask the owner first).
8. Click the blue **Schedule** button. Confirm under Content → Posts and reels → **Scheduled**. A new reel can take 20–30 s to appear; reload before assuming it failed. If it's still missing after a minute and a reload, check the other tabs before scheduling again (a second attempt can create a duplicate):
   - **In Drafts:** open it, check the caption and cover, and schedule it from there.
   - **In Published:** it went out early. Tell the owner now; don't delete it without their say.
   - **Nowhere:** schedule it once more from the start, then check Scheduled again.

## Clicking reliably
Prefer element refs from `find` over screen coordinates. Coordinates shift whenever the window is resized or the page scrolls; if you use them, take a fresh screenshot first.
