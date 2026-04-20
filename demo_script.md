# Demo Script: AI Document Intelligence Hub

**Duration:** 5 minutes  
**Target:** Sarah Chen, Compliance Manager at regional Canadian telecom  
**Demo URL:** https://ai-journey-projects-4njztxymtqnlphnqshqsnc.streamlit.app

---

## Pre-Demo Setup

**Have ready:**
- Sample telecom privacy policy PDF (50+ pages works best for impact)
- Browser open to the app, logged in
- Document Q&A tab selected
- Industry dropdown set to "Telecom"

**Upload in advance:** Have the policy already uploaded so you're not waiting during the demo. You can "re-upload" by refreshing if you want to show the upload flow.

---

## Opening (30 seconds)

**What to say:**

"Sarah, thanks for taking a few minutes. I know your time is tight, so I'll keep this short and focused on what actually matters for someone reviewing CRTC policies all day.

I'm not going to walk you through every feature — I just want to show you two things and get your honest reaction on whether this would actually help or just be another tool collecting dust."

**What to do:** Keep eye contact (or camera if virtual). Don't touch the keyboard yet.

---

## Problem Acknowledgment (45 seconds)

**What to say:**

"So here's what I keep hearing from compliance managers at regional telecoms. You get a 90-page policy document. You need to find every section that touches data retention, or CASL consent, or whatever the CRTC is asking about this week.

Right now that's Ctrl+F and a lot of scrolling. And Ctrl+F is great until you realize the document says 'information storage' instead of 'data retention' — same concept, different words, and you just missed it.

Then there's the anxiety piece. You review something, you sign off on it, and there's always that voice in the back of your head: did I miss something? Especially when you're the only one doing this work.

That's what I want to show you today — not a replacement for your judgment, but a way to be more confident in it."

**What to do:** Still not touching the app. This is about her nodding along, recognizing her own experience.

---

## Tool Walkthrough: Document Q&A (90 seconds)

**What to say:**

"Okay, so let's say you just got this privacy policy and legal wants to know what it says about data retention."

**What to click:** Make sure you're on the **Document Q&A** tab with **Telecom** selected as the industry.

**What to upload:** If not pre-loaded, upload the telecom privacy policy PDF.

"I've already uploaded it here. Instead of searching, I'm just going to ask it like I'd ask a colleague."

**What to type in the query box:**
```
What are all the data retention requirements in this policy, including any specific timeframes mentioned?
```

**What to say while it processes:**

"It's reading through the whole document now, not just keyword matching. It understands that 'retention period' and 'how long we keep your information' mean the same thing."

**When results appear:**

"See how it pulls the actual sections? It's not summarizing in a way that loses detail — it's showing you exactly where in the document this comes from. You're still the one making the call, but now you're not worried you missed page 73.

Let me try another one you'd actually need."

**What to type:**
```
What consent mechanisms does this policy describe for marketing communications under CASL?
```

**What to say:**

"This is the kind of question that would take 20 minutes of careful reading. And if you're doing five of these reviews a week, that time adds up."

**When results appear:**

"Again — it finds the relevant sections, shows you the language. You're not trusting it blindly, you're using it to make sure you didn't miss anything."

---

## Compliance Checker Demo (90 seconds)

**What to say:**

"Okay, that's finding information. But here's the part that keeps people up at night — am I actually compliant?"

**What to click:** Switch to the **Compliance Checker** tab.

**What to say:**

"This runs the same policy against actual compliance frameworks. It's checking NIST, ISO 27001, SOC 2, CIS Controls. I know you're dealing more with CRTC and CASL specifically, but the underlying security controls overlap a lot, and this catches the gaps."

**What to click:** 
- Select the uploaded document
- Click to run the compliance check

**What to say while it processes:**

"What it's doing now is mapping the policy language against control requirements. Not just 'does this document mention encryption' but 'does it actually address the control requirement around encryption at rest.'"

**When results appear:**

"So here's your gap analysis. Green means the policy addresses it adequately. Yellow means it's partially there. Red means there's a gap you need to look at.

This isn't telling you what to do — you know your environment better than any tool. But it's giving you a checklist you didn't have to build yourself. And when your CEO asks 'are we good?' after reading about another company's fine, you can show them this instead of saying 'I think so.'"

**Point to a specific gap if one shows:**

"See this one? This is the kind of thing that's easy to miss in a manual review because the policy just... doesn't mention it. There's no section to find. The gap is the absence."

---

## Close and Next Steps (45 seconds)

**What to say:**

"So that's it. Two things: find what's in the document faster, and find what's missing before an auditor does.

I'm not going to ask you to make a decision today. What I'd actually suggest is this — do you have a policy document that's been on your desk for a while? Something you've been meaning to review but haven't had time for? Send it to me, and I'll run it through and send you back the results. No commitment, no follow-up calls. Just see if the output is actually useful.

If it saves you three hours on that one document, then we can talk about what a pilot would look like. If it doesn't, no hard feelings — at least you got one policy reviewed.

What do you think? Is there something sitting in your queue right now that would be a good test?"

**What to do:** Stop talking. Let her respond. Don't fill the silence.

---

## Objection Responses (If Needed)

**"What if the AI gets something wrong?"**

"It will. No tool is perfect, and I'd never tell you to trust it blindly. The way I think about it — it's like having a junior analyst do a first pass. You're still reviewing, you're still signing off. But you're reviewing something instead of starting from a blank page. And you're catching the things it flags instead of hoping you notice them yourself."

**"We don't have budget right now."**

"Totally fair. That's why I'm suggesting the one-document test first. If it saves you real time, that's the business case you can take to your VP. 'This cut my policy review time by 60%' is a lot more compelling than anything I could put in a slide deck."

**"Does it understand Canadian regulations?"**

"The compliance frameworks are international standards right now — NIST, ISO. For CRTC-specific requirements like the Wireless Code or CCTS protocols, you'd use the Q&A side to check specific provisions. I'm working on adding Canadian telecom frameworks to the compliance checker — honestly, that's feedback I keep hearing from folks in your position. If you end up using it, your input on what frameworks matter most would actually help shape that."

**"Why not just use Google NotebookLM or ChatPDF?"**

"Great question — I've used both, actually. They're excellent for general document Q&A. If you just want to ask questions about a PDF, they work fine.

But here's what they don't do: they don't know what NIST SP 800-53 requires. They can't tell you 'your policy doesn't mention incident response timeframes, and that's a gap against control IR-4.' They're not mapping your document against compliance frameworks — they're just answering questions about what's written.

The other piece is the telecom context. When I set this to Telecom mode, it understands that 'customer proprietary network information' isn't just a random phrase — it knows CPNI has specific regulatory requirements. It knows what CASL consent looks like versus generic marketing opt-in. That's not generic AI — that's industry-specific prompting built from working with compliance teams like yours.

And honestly? NotebookLM doesn't come with me. If you hit an edge case, or you want to add a new framework, or the output doesn't make sense — you're on your own. With this, you're getting a tool and a consultant who understands what you're actually trying to accomplish. That's harder to quantify, but it's usually what makes the difference between something that gets used and something that sits in a bookmark folder."

---

## Post-Demo

- Send a brief email thanking her for her time
- Attach nothing. Don't send a deck or pricing
- Ask again if she has a document she'd like to test
- Follow up in one week only if she sent a document
