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




```
┣ 📂data
 ┣ 📂src
 ┃ ┣ 📂camera_layer
 ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┣ 📜__init__.cpython-310.pyc
 ┃ ┃ ┃ ┣ 📜base_camera.cpython-310.pyc
 ┃ ┃ ┃ ┣ 📜camera_factory.cpython-310.pyc
 ┃ ┃ ┃ ┣ 📜camera_manager.cpython-310.pyc
 ┃ ┃ ┃ ┣ 📜file_camera.cpython-310.pyc
 ┃ ┃ ┃ ┣ 📜mobile_camera.cpython-310.pyc
 ┃ ┃ ┃ ┣ 📜rtsp_camera.cpython-310.pyc
 ┃ ┃ ┃ ┗ 📜webcam_camera.cpython-310.pyc
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜base_camera.py
 ┃ ┃ ┣ 📜camera_factory.py
 ┃ ┃ ┣ 📜camera_manager.py
 ┃ ┃ ┣ 📜file_camera.py
 ┃ ┃ ┣ 📜mobile_camera.py
 ┃ ┃ ┣ 📜rtsp_camera.py
 ┃ ┃ ┗ 📜webcam_camera.py
 ┃ ┣ 📂edge_processing
 ┃ ┃ ┣ 📂detection
 ┃ ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┃ ┣ 📜__init__.cpython-310.pyc
 ┃ ┃ ┃ ┃ ┣ 📜detection_manager.cpython-310.pyc
 ┃ ┃ ┃ ┃ ┣ 📜detection_packet.cpython-310.pyc
 ┃ ┃ ┃ ┃ ┗ 📜yolov8_detector.cpython-310.pyc
 ┃ ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┃ ┣ 📜detection_manager.py
 ┃ ┃ ┃ ┣ 📜detection_packet.py
 ┃ ┃ ┃ ┗ 📜yolov8_detector.py
 ┃ ┃ ┣ 📂frame_capture
 ┃ ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┃ ┣ 📜__init__.cpython-310.pyc
 ┃ ┃ ┃ ┃ ┣ 📜fps_controller.cpython-310.pyc
 ┃ ┃ ┃ ┃ ┣ 📜frame_buffer.cpython-310.pyc
 ┃ ┃ ┃ ┃ ┣ 📜frame_dispatcher.cpython-310.pyc
 ┃ ┃ ┃ ┃ ┗ 📜frame_packet.cpython-310.pyc
 ┃ ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┃ ┣ 📜fps_controller.py
 ┃ ┃ ┃ ┣ 📜frame_buffer.py
 ┃ ┃ ┃ ┣ 📜frame_dispatcher.py
 ┃ ┃ ┃ ┗ 📜frame_packet.py
 ┃ ┃ ┣ 📂gnn
 ┃ ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┃ ┣ 📜__init__.cpython-310.pyc
 ┃ ┃ ┃ ┃ ┣ 📜msgat_manager.cpython-310.pyc
 ┃ ┃ ┃ ┃ ┗ 📜msgat_model.cpython-310.pyc
 ┃ ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┃ ┣ 📜msgat_manager.py
 ┃ ┃ ┃ ┗ 📜msgat_model.py
 ┃ ┃ ┣ 📂graph
 ┃ ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┃ ┣ 📜__init__.cpython-310.pyc
 ┃ ┃ ┃ ┃ ┣ 📜graph_manager.cpython-310.pyc
 ┃ ┃ ┃ ┃ ┣ 📜interaction_graph.cpython-310.pyc
 ┃ ┃ ┃ ┃ ┗ 📜motion_memory.cpython-310.pyc
 ┃ ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┃ ┣ 📜graph_manager.py
 ┃ ┃ ┃ ┣ 📜interaction_graph.py
 ┃ ┃ ┃ ┗ 📜motion_memory.py
 ┃ ┃ ┣ 📂pose_estimation
 ┃ ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┃ ┣ 📜__init__.cpython-310.pyc
 ┃ ┃ ┃ ┃ ┣ 📜mediapipe_pose.cpython-310.pyc
 ┃ ┃ ┃ ┃ ┣ 📜pose_manager.cpython-310.pyc
 ┃ ┃ ┃ ┃ ┗ 📜pose_packet.cpython-310.pyc
 ┃ ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┃ ┣ 📜mediapipe_pose.py
 ┃ ┃ ┃ ┣ 📜pose_manager.py
 ┃ ┃ ┃ ┗ 📜pose_packet.py
 ┃ ┃ ┣ 📂reid
 ┃ ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┃ ┣ 📜__init__.cpython-310.pyc
 ┃ ┃ ┃ ┃ ┣ 📜appearance_encoder.cpython-310.pyc
 ┃ ┃ ┃ ┃ ┗ 📜global_identity_manager.cpython-310.pyc
 ┃ ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┃ ┣ 📜appearance_encoder.py
 ┃ ┃ ┃ ┗ 📜global_identity_manager.py
 ┃ ┃ ┣ 📂temporal
 ┃ ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┃ ┣ 📜__init__.cpython-310.pyc
 ┃ ┃ ┃ ┃ ┣ 📜temporal_manager.cpython-310.pyc
 ┃ ┃ ┃ ┃ ┗ 📜temporal_memory.cpython-310.pyc
 ┃ ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┃ ┣ 📜temporal_manager.py
 ┃ ┃ ┃ ┗ 📜temporal_memory.py
 ┃ ┃ ┗ 📂tracking
 ┃ ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┃ ┣ 📜__init__.cpython-310.pyc
 ┃ ┃ ┃ ┃ ┣ 📜deepsort_tracker.cpython-310.pyc
 ┃ ┃ ┃ ┃ ┣ 📜simple_tracker.cpython-310.pyc
 ┃ ┃ ┃ ┃ ┣ 📜track_packet.cpython-310.pyc
 ┃ ┃ ┃ ┃ ┗ 📜tracking_manager.cpython-310.pyc
 ┃ ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┃ ┣ 📜deepsort_tracker.py
 ┃ ┃ ┃ ┣ 📜simple_tracker.py
 ┃ ┃ ┃ ┣ 📜track_packet.py
 ┃ ┃ ┃ ┗ 📜tracking_manager.py
 ┃ ┣ 📂tests
 ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┗ 📜test_cameras.cpython-310.pyc
 ┃ ┃ ┗ 📜test_cameras.py
 ┃ ┣ 📂utils
 ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┣ 📜camera_worker.cpython-310.pyc
 ┃ ┃ ┃ ┣ 📜display_worker.cpython-310.pyc
 ┃ ┃ ┃ ┣ 📜pipeline_queue.cpython-310.pyc
 ┃ ┃ ┃ ┗ 📜processing_worker.cpython-310.pyc
 ┃ ┃ ┣ 📜camera_worker.py
 ┃ ┃ ┣ 📜display_worker.py
 ┃ ┃ ┣ 📜pipeline_queue.py
 ┃ ┃ ┗ 📜processing_worker.py
 ┃ ┣ 📜main.py
 ┃ ┗ 📜yolov8n.pt
 ┣ 📜.gitignore
 ┣ 📜LICENSE
 ┣ 📜README.md
 ┣ 📜doc.md
 ┣ 📜requirements.txt
 ┣ 📜structure.md
 ┗ 📜yolov8n.pt
```



<pre id="tree-panel"><br/> ┣ data<br/> ┣ src<br/> ┃ ┣ camera_layer<br/> ┃ ┃ ┣ __pycache__<br/> ┃ ┃ ┃ ┣ __init__.cpython-310.pyc<br/> ┃ ┃ ┃ ┣ base_camera.cpython-310.pyc<br/> ┃ ┃ ┃ ┣ camera_factory.cpython-310.pyc<br/> ┃ ┃ ┃ ┣ camera_manager.cpython-310.pyc<br/> ┃ ┃ ┃ ┣ file_camera.cpython-310.pyc<br/> ┃ ┃ ┃ ┣ mobile_camera.cpython-310.pyc<br/> ┃ ┃ ┃ ┣ rtsp_camera.cpython-310.pyc<br/> ┃ ┃ ┃ ┗ webcam_camera.cpython-310.pyc<br/> ┃ ┃ ┣ __init__.py<br/> ┃ ┃ ┣ base_camera.py<br/> ┃ ┃ ┣ camera_factory.py<br/> ┃ ┃ ┣ camera_manager.py<br/> ┃ ┃ ┣ file_camera.py<br/> ┃ ┃ ┣ mobile_camera.py<br/> ┃ ┃ ┣ rtsp_camera.py<br/> ┃ ┃ ┗ webcam_camera.py<br/> ┃ ┣ edge_processing<br/> ┃ ┃ ┣ detection<br/> ┃ ┃ ┃ ┣ __pycache__<br/> ┃ ┃ ┃ ┃ ┣ __init__.cpython-310.pyc<br/> ┃ ┃ ┃ ┃ ┣ detection_manager.cpython-310.pyc<br/> ┃ ┃ ┃ ┃ ┣ detection_packet.cpython-310.pyc<br/> ┃ ┃ ┃ ┃ ┗ yolov8_detector.cpython-310.pyc<br/> ┃ ┃ ┃ ┣ __init__.py<br/> ┃ ┃ ┃ ┣ detection_manager.py<br/> ┃ ┃ ┃ ┣ detection_packet.py<br/> ┃ ┃ ┃ ┗ yolov8_detector.py<br/> ┃ ┃ ┣ frame_capture<br/> ┃ ┃ ┃ ┣ __pycache__<br/> ┃ ┃ ┃ ┃ ┣ __init__.cpython-310.pyc<br/> ┃ ┃ ┃ ┃ ┣ fps_controller.cpython-310.pyc<br/> ┃ ┃ ┃ ┃ ┣ frame_buffer.cpython-310.pyc<br/> ┃ ┃ ┃ ┃ ┣ frame_dispatcher.cpython-310.pyc<br/> ┃ ┃ ┃ ┃ ┗ frame_packet.cpython-310.pyc<br/> ┃ ┃ ┃ ┣ __init__.py<br/> ┃ ┃ ┃ ┣ fps_controller.py<br/> ┃ ┃ ┃ ┣ frame_buffer.py<br/> ┃ ┃ ┃ ┣ frame_dispatcher.py<br/> ┃ ┃ ┃ ┗ frame_packet.py<br/> ┃ ┃ ┣ gnn<br/> ┃ ┃ ┃ ┣ __pycache__<br/> ┃ ┃ ┃ ┃ ┣ __init__.cpython-310.pyc<br/> ┃ ┃ ┃ ┃ ┣ msgat_manager.cpython-310.pyc<br/> ┃ ┃ ┃ ┃ ┗ msgat_model.cpython-310.pyc<br/> ┃ ┃ ┃ ┣ __init__.py<br/> ┃ ┃ ┃ ┣ msgat_manager.py<br/> ┃ ┃ ┃ ┗ msgat_model.py<br/> ┃ ┃ ┣ graph<br/> ┃ ┃ ┃ ┣ __pycache__<br/> ┃ ┃ ┃ ┃ ┣ __init__.cpython-310.pyc<br/> ┃ ┃ ┃ ┃ ┣ graph_manager.cpython-310.pyc<br/> ┃ ┃ ┃ ┃ ┣ interaction_graph.cpython-310.pyc<br/> ┃ ┃ ┃ ┃ ┗ motion_memory.cpython-310.pyc<br/> ┃ ┃ ┃ ┣ __init__.py<br/> ┃ ┃ ┃ ┣ graph_manager.py<br/> ┃ ┃ ┃ ┣ interaction_graph.py<br/> ┃ ┃ ┃ ┗ motion_memory.py<br/> ┃ ┃ ┣ pose_estimation<br/> ┃ ┃ ┃ ┣ __pycache__<br/> ┃ ┃ ┃ ┃ ┣ __init__.cpython-310.pyc<br/> ┃ ┃ ┃ ┃ ┣ mediapipe_pose.cpython-310.pyc<br/> ┃ ┃ ┃ ┃ ┣ pose_manager.cpython-310.pyc<br/> ┃ ┃ ┃ ┃ ┗ pose_packet.cpython-310.pyc<br/> ┃ ┃ ┃ ┣ __init__.py<br/> ┃ ┃ ┃ ┣ mediapipe_pose.py<br/> ┃ ┃ ┃ ┣ pose_manager.py<br/> ┃ ┃ ┃ ┗ pose_packet.py<br/> ┃ ┃ ┣ reid<br/> ┃ ┃ ┃ ┣ __pycache__<br/> ┃ ┃ ┃ ┃ ┣ __init__.cpython-310.pyc<br/> ┃ ┃ ┃ ┃ ┣ appearance_encoder.cpython-310.pyc<br/> ┃ ┃ ┃ ┃ ┗ global_identity_manager.cpython-310.pyc<br/> ┃ ┃ ┃ ┣ __init__.py<br/> ┃ ┃ ┃ ┣ appearance_encoder.py<br/> ┃ ┃ ┃ ┗ global_identity_manager.py<br/> ┃ ┃ ┣ temporal<br/> ┃ ┃ ┃ ┣ __pycache__<br/> ┃ ┃ ┃ ┃ ┣ __init__.cpython-310.pyc<br/> ┃ ┃ ┃ ┃ ┣ temporal_manager.cpython-310.pyc<br/> ┃ ┃ ┃ ┃ ┗ temporal_memory.cpython-310.pyc<br/> ┃ ┃ ┃ ┣ __init__.py<br/> ┃ ┃ ┃ ┣ temporal_manager.py<br/> ┃ ┃ ┃ ┗ temporal_memory.py<br/> ┃ ┃ ┗ tracking<br/> ┃ ┃ ┃ ┣ __pycache__<br/> ┃ ┃ ┃ ┃ ┣ __init__.cpython-310.pyc<br/> ┃ ┃ ┃ ┃ ┣ deepsort_tracker.cpython-310.pyc<br/> ┃ ┃ ┃ ┃ ┣ simple_tracker.cpython-310.pyc<br/> ┃ ┃ ┃ ┃ ┣ track_packet.cpython-310.pyc<br/> ┃ ┃ ┃ ┃ ┗ tracking_manager.cpython-310.pyc<br/> ┃ ┃ ┃ ┣ __init__.py<br/> ┃ ┃ ┃ ┣ deepsort_tracker.py<br/> ┃ ┃ ┃ ┣ simple_tracker.py<br/> ┃ ┃ ┃ ┣ track_packet.py<br/> ┃ ┃ ┃ ┗ tracking_manager.py<br/> ┃ ┣ tests<br/> ┃ ┃ ┣ __pycache__<br/> ┃ ┃ ┃ ┗ test_cameras.cpython-310.pyc<br/> ┃ ┃ ┗ test_cameras.py<br/> ┃ ┣ utils<br/> ┃ ┃ ┣ __pycache__<br/> ┃ ┃ ┃ ┣ camera_worker.cpython-310.pyc<br/> ┃ ┃ ┃ ┣ display_worker.cpython-310.pyc<br/> ┃ ┃ ┃ ┣ pipeline_queue.cpython-310.pyc<br/> ┃ ┃ ┃ ┗ processing_worker.cpython-310.pyc<br/> ┃ ┃ ┣ camera_worker.py<br/> ┃ ┃ ┣ display_worker.py<br/> ┃ ┃ ┣ pipeline_queue.py<br/> ┃ ┃ ┗ processing_worker.py<br/> ┃ ┣ main.py<br/> ┃ ┗ yolov8n.pt<br/> ┣ .gitignore<br/> ┣ LICENSE<br/> ┣ README.md<br/> ┣ doc.md<br/> ┣ requirements.txt<br/> ┣ structure.md<br/> ┗ yolov8n.pt</pre>
