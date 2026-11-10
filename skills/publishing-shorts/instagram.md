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
4. Caption: type the body, then **each hashtag as its own typing action**, then click outside the box. Zoom in and verify; the autocomplete can merge tags.
5. Thumbnail → Choose suggested: pick the frame showing the hook caption. Wait for "Your reel is safe to publish".
6. Next (Edit: no audio) → Next (Share) → **Schedule**:
   - Date picker: click the day.
   - Time: click the hour segment and type `19`, then click the minute segment and type `30`. Verify.
7. Click **Schedule**. Confirm under Content → Posts and reels → **Scheduled**; the reel shows "Processing…" at first.
