MCAD/
│
├── README.md
├── requirements.txt
├── setup.sh
│
├── configs/                         # All experiment & system configs
│   ├── cameras.yaml
│   ├── model.yaml
│   ├── tracking.yaml
│   ├── training.yaml
│   └── system.yaml
│
├── data/
│   ├── raw/                          # Raw camera streams / videos
│   ├── processed/                   # Extracted frames, poses, tracks
│   ├── annotations/                 # Labels (if any)
│   └── synthetic/                   # Generated anomalies (GBS-MFA)
│
├── src/
│   ├── main.py                      # Pipeline entry point
│   │
│   ├── camera_layer/                # 📷 CAMERA LAYER
│   │   ├── __init__.py
│   │   ├── ip_camera.py
│   │   ├── stream_manager.py
│   │   └── camera_registry.py
│   │
│   ├── edge_processing/             # ⚡ EDGE / GPU PIPELINE
│   │   ├── __init__.py
│   │   │
│   │   ├── frame_capture/           # Stage 1
│   │   │   ├── capture.py
│   │   │   └── buffer.py
│   │   │
│   │   ├── detection/               # Stage 2
│   │   │   ├── yolov8_detector.py
│   │   │   └── detector_utils.py
│   │   │
│   │   ├── tracking/                # Stage 3
│   │   │   ├── deepsort_tracker.py
│   │   │   └── track_manager.py
│   │   │
│   │   ├── pose_estimation/          # Stage 4
│   │   │   ├── mediapipe_pose.py
│   │   │   └── pose_features.py
│   │   │
│   │   ├── graph/                   # Stage 5
│   │   │   ├── graph_constructor.py
│   │   │   ├── spatial_edges.py
│   │   │   └── temporal_edges.py
│   │   │
│   │   ├── interaction_model/       # Stage 6 (MS-GAT)
│   │   │   ├── msgat.py
│   │   │   ├── attention_layers.py
│   │   │   └── interaction_features.py
│   │   │
│   │   ├── anomaly_modules/         # Stage 7
│   │   │   ├── nebe.py
│   │   │   ├── sticl.py
│   │   │   ├── gbs_mfa.py
│   │   │   └── rl_dcat.py
│   │   │
│   │   ├── fusion/                  # Stage 8
│   │   │   ├── anomaly_fusion.py
│   │   │   └── scoring.py
│   │   │
│   │   └── utils/
│   │       ├── logger.py
│   │       ├── visualizer.py
│   │       └── time_sync.py
│
├── training/                         # Training & experiments
│   ├── train_msgat.py
│   ├── train_nebe.py
│   ├── train_rl_dcat.py
│   └── evaluation.py
│
├── dashboard/                        # 🖥 Application Layer
│   ├── app.py                       # Streamlit Dashboard
│   ├── components/
│   └── plots.py
│
├── alerts/
│   ├── alert_manager.py
│   ├── email_alert.py
│   └── webhook.py
│
├── experiments/
│   ├── ablation/
│   ├── benchmarks/
│   └── logs/
│
├── docs/                             # Review + Paper + UML
│   ├── architecture/
│   ├── uml/
│   ├── figures/
│   └── ieee_notes.md
│
└── tests/
    ├── test_detection.py
    ├── test_tracking.py
    ├── test_graph.py
    └── test_pipeline.py
