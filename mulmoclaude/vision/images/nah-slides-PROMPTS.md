# nah-slide*-final-169.png — 生成記録 / Generation record

`nah-slideN-final-169.png` は「我が家で育てるAIアシスタント」デッキ(`mulmoclaude/vision/nurtured-at-home_ja.json`)の各スライド完成画。ホワイトボードアニメ化(PR #47)の際に、動画の終端フレーム(lastFrameImageName)として固定するためここにチェックインした。元は同スクリプトの imagePrompt ビートとして gpt-image-2 が生成したもの(1536×1024)を、16:9 にパディングしたもの。

## 生成条件

- モデル: OpenAI `gpt-image-2`(provider: openai)
- 各プロンプトには下記の共通スタイル文字列が連結される(imageParams.style):

> Whiteboard marker drawing: a hand-drawn sketch on a clean white dry-erase whiteboard, drawn with black, blue, red and green marker pens. Rough but confident strokes, simple diagrams, boxes, arrows, stick figures, underlines and quick handwritten labels. Slight marker texture, a few faint eraser smudges. Flat, bright, evenly lit, full-bleed white background. No photorealism, no gradients, no 3D rendering, no watercolor.

- 16:9化: `ffmpeg -i <src> -vf "scale=1080:720,pad=1280:720:100:0:color=0xF7F6F4" <dst>`
- `nah-blank-whiteboard.png`: 生成物ではなく単色画像。`ffmpeg -f lavfi -i color=0xF7F6F4:s=1280x720 -frames:v 1`

## スライド別 imagePrompt

### nah-slide1-final-169.png

A store shelf drawn in marker with an empty spot and a crossed-out price tag, handwritten label 'NOT FOR SALE' in red. Next to it, a stick figure imagines a friendly little robot assistant in a thought bubble, with a small red heart.

### nah-slide2-final-169.png

A stick figure lovingly watering a small green sprout that grows out of an open laptop. A simple house outline drawn around them, a smiling sun in the top corner. Handwritten label 'HOME' underlined in red, and a small Japanese handwritten label 我が家 next to it.

### nah-slide3-final-169.png

A timeline arrow from left to right: on the left a brain sketch labeled 'Model' with a small trophy, on the right a tall growing stack of papers and folders labeled 'Memory'. A big blue arrow curving from the brain to the stack labeled 'the race moved'.

### nah-slide4-final-169.png

A big layered pile drawn in marker, layers labeled 'Conversations', 'Preferences', 'Records', 'Apps', with a red underlined heading 'YOUR pile'. Below it, a small box with a gear labeled 'Model = engine', drawn deliberately small.

### nah-slide5-final-169.png

Two small scenes side by side: a stick figure carefully carrying chat bubbles into a box labeled 'backup', and another stick figure shielding a small robot from a trash can, saying 'No!' in a speech bubble. A green handwritten label 'raising, not using' underlined.

### nah-slide6-final-169.png

A stick figure with a ball and chain: the ball is a huge pile of folders and hearts labeled 'your data', sitting inside a cloud labeled 'their server'. An arrow pointing away labeled 'switch?' is crossed out in red.

### nah-slide7-final-169.png

Two warning panels drawn in marker with red triangle warning signs. Left: a funnel siphoning droplets from a stick figure's head into a big corporate robot, labeled 'siphoning'. Right: folders and a small app window locked inside a barred cage with a padlock, labeled 'captivity'.

### nah-slide8-final-169.png

A small moving box labeled 'memory export' carried by a stick figure out of one cloud toward another cloud, with a green checkmark and the handwritten word 'Portability' underlined in green.

### nah-slide9-final-169.png

(v2 — ラベルを赤字の一言だけに削減、アプリはアイコンで表現。アニメーション化で文字が潰れたため)

A moving truck driving away carrying one small cardboard box. Left behind on the curb: two sketched app windows (one showing a fork and knife icon, one showing a simple table of numbers), a red alarm clock, and a small booklet. A big red arrow points at the left-behind items with one short handwritten note: 'these don't move!'. No other text or labels anywhere.

### nah-slide10-final-169.png

(v2 — 文字を1語に削減、日本語を除去。アニメーション化で文字が崩れたため)

A big warm house outline drawn in black marker, sheltering a few folders, two small app windows and a green sprout inside. A smiling sun in the top corner. Below the house, one single large handwritten word 'HOME', underlined in red. No other text or labels anywhere.

### nah-slide11-final-169.png

A checklist with four numbered checkboxes, each with a green check and a tiny icon: 1 a folder on a laptop labeled 'your files', 2 an open padlock labeled 'open source', 3 a gear on a laptop labeled 'runs locally', 4 two phones connected by a dotted line through a circle labeled 'relay' with a crossed-out database symbol labeled 'stores nothing'.

### nah-slide12-final-169.png

A stick figure with a speech bubble showing a tiny fork, knife and list sketch saying 'Restaurant list!'. A friendly robot writing on a sheet of paper labeled 'Blueprint'. A crossed-out code symbol '</>' with a red handwritten note 'no code!'. Handwritten 'MulmoClaude' in a corner.

### nah-slide13-final-169.png

A flow diagram: a box labeled 'AI' with an arrow labeled 'writes' pointing to a sheet of paper labeled 'Blueprint (Schema)', then an arrow to a box labeled 'HOST', which points to a sketched browser window labeled 'App'. Underneath, a handwritten slogan underlined in green: 'Blueprint = App, AI = Author, Host = Runner'.

### nah-slide14-final-169.png

A robot writing a letter at a desk, the envelope addressed 'To: future me'. Next to it an open notebook labeled 'Manual' with a sketched bullet list: 'when?', 'what?', 'don'ts'. A small lightbulb above the robot's head.

### nah-slide15-final-169.png

A stick figure with a speech bubble containing a steaming ramen bowl sketch and a checkmark. A robot reading a small booklet labeled 'Manual' with a lightbulb above its head. Below, an open folder with plain white file sheets spilling out, and a stick figure peeking inside happily.

### nah-slide16-final-169.png

Three safety devices drawn side by side like shields: 1 a gate with a big red X stamped over a torn blueprint labeled 'broken? rejected', 2 a single bad file with a frowny face placed alone inside a small quarantine box apart from a healthy stack, labeled 'quarantined', 3 a code symbol '</>' inside a barred cage, labeled 'in a cage'. Heading handwritten: '3 safety devices'.

### nah-slide17-final-169.png

A close-up of a barred cage drawn in black marker containing a small screen showing a sketched map with a location pin and a bar chart. A hand passes a single card through a narrow slot in the bars, the slot labeled 'allowed data only'. A green checkmark beside the slot.

### nah-slide18-final-169.png

A test scoreboard drawn in marker: a tally counter labeled '72 tests', a huge green '0' labeled 'broken apps that ran', and a checklist of green checkmarks with one red X circled, with a handwritten note 'fixed in 1 try' and a small arrow.

### nah-slide19-final-169.png

A sad, empty chat window sketch with a single speech bubble reading 'Your reading list was empty until just now.' Next to it a robot with a control panel of toggle switches flipped to OFF, labeled 'memory', 'reminders', 'checks'. Handwritten label in red: 'empty chatbot'.

### nah-slide20-final-169.png

(v2 — ラベルを1語に削減。アニメーション化で文字が崩れたため)

Moving day: a small moving truck driving away from a full, lively house toward an empty house in the distance. The truck carries a single small box. A few unlabeled boxes and an alarm clock left behind on the curb. The only text in the drawing is one handwritten word 'memories' on the truck's box.

### nah-slide21-final-169.png

Inside a new, bare house: a robot with a thought bubble containing a smiling stick figure portrait labeled 'I remember you'. Around it, empty shelves, a crossed-out alarm clock, an empty picture frame. Speech bubble from the robot: 'I recall the reminder... but I can't deliver it.'

### nah-slide22-final-169.png

A two-column comparison drawn in marker: left column headed 思い出 with 'Memories' under it, a small photo album sketch and a big green checkmark labeled 'moves'; right column headed 能力 with 'Abilities' under it, a gear and alarm clock sketch and a big red X labeled 'does not move'. A thick red underline across the bottom.

### nah-slide23-final-169.png

A laptop with a single big folder on its screen labeled 'everything', an arrow copying the folder to an external hard drive with a green check labeled 'backup = copy'. A small tag beside it labeled 'git' with a clock-and-history spiral icon.

### nah-slide24-final-169.png

A friendly robot body labeled 'Workspace' with an open hatch on its chest; a small crane swaps engine blocks in and out. Three engine blocks on the floor labeled 'Claude Code', 'GPT (beta)', 'Open (planned)'. A handwritten note with an arrow to the robot: 'your pile stays'.

### nah-slide25-final-169.png

A fork in the road drawn in marker: the wide left path leads to a huge cloud with corporate buildings labeled 'default', the narrow right path leads to a small warm house with a sprout, labeled 'HOME'. A stick figure at the fork stepping onto the right path.

### nah-slide26-final-169.png

A stick figure and a small friendly robot standing side by side in front of a house at sunrise, the sun drawn with red marker rays. Large handwritten Japanese text across the top: 育てるのは、あなた自身 underlined in red. Small handwritten 'MulmoClaude' in the bottom corner.
