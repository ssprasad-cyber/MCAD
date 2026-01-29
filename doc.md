# 🚀 STAGE 1 — MULTI-CAMERA FRAME INGESTION (FOUNDATION)

This stage is  **NON-NEGOTIABLE** .

If this is solid,  **everything above it becomes easy** .

---

## 🎯 STAGE 1 GOAL

> Build a **camera-agnostic, multi-camera frame ingestion system** that:

* Works with **video files**
* Works with **webcam**
* Works with **mobile / RTSP**
* Outputs **standardized frame packets**
* Is **CUDA-ready but not CUDA-dependent**

No ML yet. No YOLO. No tracking.

Just  **clean frame flow** .

---

# 📁 FILES TO CREATE (STAGE 1 ONLY)

Create this structure:

src/camera_layer/
├── __init__.py
├── base_camera.py        # Abstract interface
├── file_camera.py        # Video file as camera
├── webcam_camera.py     # Laptop / USB webcam
├── mobile_camera.py     # Mobile IP camera
├── rtsp_camera.py       # CCTV / IP cam
├── camera_factory.py    # Creates cameras from config
└── camera_manager.py    # Handles multiple cameras

---

# 🧠 CORE DESIGN PRINCIPLE

> **Pipeline NEVER knows camera type**
>
> Everything speaks in **FramePacket**

<pre class="overflow-visible! px-0!" data-start="1047" data-end="1148"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>FramePacket = {
    </span><span>"camera_id"</span><span>: </span><span>str</span><span>,
    </span><span>"frame"</span><span>: np.ndarray,
    </span><span>"timestamp"</span><span>: </span><span>float</span><span>
}
</span></span></code></div></div></pre>

This will stay the same till anomaly fusion.


# 🚀 STAGE 2 — FRAME BUFFERING & RATE CONTROL

( **Decoupling Camera I/O from Processing** )

---

## 🎯 STAGE 2 PURPOSE (VERY CLEAR)

> STAGE 2 sits **between camera_layer and ML pipeline**
>
> It **absorbs irregular camera input** and outputs  **stable, controllable frame flow** .

If Stage 1 = *frame acquisition*

Stage 2 = *frame stabilization*

---

## ❓ WHY STAGE 2 IS REQUIRED

Real cameras (and videos) have:

* Different FPS
* Network jitter (mobile / RTSP)
* Blocking reads
* Burst behavior

If you skip this:

* YOLO will lag
* GPU will idle or overload
* Multi-camera sync breaks

---

## 🧠 RESPONSIBILITY SPLIT (IMPORTANT)

| Layer             | Responsibility            |
| ----------------- | ------------------------- |
| `camera_layer`  | Acquire frames            |
| **Stage 2** | Buffer, drop, pace frames |
| Stage 3+          | ML & logic                |

Camera layer must **never** know about FPS, buffers, or threading.

---

# 📁 STAGE 2 FILE STRUCTURE

<pre class="overflow-visible! px-0!" data-start="1046" data-end="1244"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>src</span><span>/
└── edge_processing/
    └── frame_capture/
        ├── __init__</span><span>.py</span><span>
        ├── frame_packet</span><span>.py</span><span>
        ├── frame_buffer</span><span>.py</span><span>
        ├── frame_dispatcher</span><span>.py</span><span>
        └── fps_controller</span><span>.py</span><span>
</span></span></code></div></div></pre>

---

# ✅ STAGE 3 — OBJECT DETECTION (YOLOv8 + CUDA)

## 🎯 STAGE 3 PURPOSE (ONE LINE)

> Consume **FPS-controlled FramePackets** and output **detected objects per camera frame** using CUDA-accelerated YOLOv8.

No tracking yet.

No pose yet.

Only  **detection** .

---

## 📦 INPUT → OUTPUT CONTRACT (VERY IMPORTANT)

### Input (from Stage 2)

<pre class="overflow-visible! px-0!" data-start="599" data-end="690"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>FramePacket {
    camera_id: </span><span>str</span><span>
    frame: np.ndarray
    timestamp: </span><span>float</span><span>
}
</span></span></code></div></div></pre>

### Output (Stage 3)

<pre class="overflow-visible! px-0!" data-start="713" data-end="818"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>DetectionPacket {
    camera_id: </span><span>str</span><span>
    timestamp: </span><span>float</span><span>
    detections: </span><span>List</span><span>[Detection]
}
</span></span></code></div></div></pre>

Where each detection is:

<pre class="overflow-visible! px-0!" data-start="845" data-end="952"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>{
  </span><span>"bbox"</span><span>: [x1, y1, x2, y2],
  </span><span>"confidence"</span><span>: </span><span>float</span><span>,
  </span><span>"class_id"</span><span>: </span><span>int</span><span>,
  </span><span>"class_name"</span><span>: </span><span>str</span><span>
}
</span></span></code></div></div></pre>

This  **contract is locked** .

---

# 📁 STAGE 3 FILE STRUCTURE

<pre class="overflow-visible! px-0!" data-start="1018" data-end="1190"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>src/
└── edge_processing/
    └── detection/
        ├── </span><span>__init__</span><span>.py
        ├── detection_packet.py
        ├── yolov8_detector.py
        └── detection_manager.py</span></span></code></div></div></pre>
