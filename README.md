# Classroom Capture Streamlit App

A streamlined Streamlit application for capturing class observations with photos, video, audio notes (auto-transcribed with Whisper), and optional typed notes. Media is organised by class and date, and each class has a dedicated gallery page for quick review.

## Features

- Mobile-friendly recorder page with compact controls for class selection, date, media uploads, and voice/text notes.
- Audio recording directly in the browser using [`audio-recorder-streamlit`](https://github.com/Joooohan/audio-recorder-streamlit).
- Automatic speech-to-text via [Faster Whisper](https://github.com/guillaumekln/faster-whisper) with typed note fallback when recording isn't possible.
- Galleries for AP Chemistry, Chemistry, and PLTW Medical Interventions with entries grouped by date and displayed as lightweight cards.
- Persistent storage under `data/<class>/<date>/<entry>` so files survive restarts when mounted to a Fly.io volume.

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run Home.py
```

By default data is saved in `./data`. Set the `DATA_ROOT` environment variable to change the persistence directory.

### Whisper configuration

The app uses Faster Whisper for transcription. You can control the model with environment variables:

- `WHISPER_MODEL_SIZE` (default: `small`)
- `WHISPER_COMPUTE_TYPE` (default: `int8_float16`)
- `WHISPER_DEVICE` (default: `cpu`)

Ensure the server has enough memory for the chosen model. If transcription fails, the audio clip is still saved and the UI will display a helpful notice.

## Deployment on Fly.io

1. Install the Fly.io CLI and authenticate: `fly auth login`.
2. Rename the `app` value in `fly.toml` to your chosen application slug.
3. Create a volume to persist media: `fly volumes create class_data --size 5 --region <REGION>`.
4. Deploy using the bundled Dockerfile:

   ```bash
   fly deploy
   ```

Fly will mount the `class_data` volume at `/app/data`, keeping uploads and transcripts safe across restarts. The container listens on port `8080` internally and is exposed via Fly's edge network.

### Deploying from the Fly.io dashboard or GitHub integration

The provided `fly.toml` targets the newer **Machines** platform (it uses an `[http_service]` section). When launching directly from the Fly UI or GitHub integration, make sure the app is created as a Machines application; otherwise Fly will attempt to use the legacy Nomad platform and show the error:

```
launch manifest was created for a ... app, but this is a ... app
```

To deploy from the dashboard:

1. Create a new application in the UI and choose **Machines** as the platform.
2. Attach a volume named `class_data` in the target region so uploads persist.
3. Point the deployment to this repository and keep the detected Dockerfile buildpack.

After the first deployment you can use the dashboard or GitHub integration for subsequent releases. If you already created a Nomad app, run `fly apps destroy <name>` and recreate it as a Machines app, or deploy from your local terminal with `fly launch --from` which will prompt for the correct platform.

## Project structure

- `Home.py` – recorder interface for capturing media and notes.
- `pages/` – individual gallery pages for each class.
- `app/` – shared helpers for storage, gallery rendering, transcription, and styling.
- `data/` – created at runtime to store uploaded media (ignored by Git).

## License

This project is released under the terms of the [MIT License](LICENSE).
