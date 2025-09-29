# Multi-Camera Spatiotemporal Deep Learning Framework for Real-Time Abnormal Behavior Detection in Dense Urban Environments

## Overview

This repository contains the implementation of a **comprehensive spatiotemporal deep learning framework** for **real-time abnormal behavior detection** in crowded urban environments using multi-camera surveillance. Our hybrid architecture addresses key challenges of existing systems, including poor generalization, high computational cost, and high false positive rates.

By combining **graph attention networks, reinforcement learning, contrastive learning, neuromorphic event encoding, and generative behavior synthesis**, this framework sets a **new benchmark** for scalable, adaptable, and computationally efficient urban surveillance.

## Authors

Sai Babu Veesam, B. Tarakeswara Rao, Zarina Begum, R. S. M. Lakshmi Patibandla, Arvin Arun Dcosta, Shonak Bansal, Krishna Prakash, Mohammad Rashed Iqbal Faruque, & K. S. Al-mugren.

## Keywords

Anomaly detection, Graph attention networks, Multi-camera surveillance, Reinforcement learning, Spatiotemporal learning.

---

## 1. Problem Statement

Modern urban environments require robust multi-camera surveillance for anomaly detection. Current approaches face:

* **Detection Failures** due to occlusion, scene dynamics, and computational inefficiency.
* **High False Positives**, making automated monitoring unreliable.
* **Poor Generalization** to rare/unseen events due to limited spatiotemporal modeling.
* **Inefficient Resource Utilization** across cameras, leading to redundant computation.
* **Human Supervision Dependency**, which is error-prone and unscalable.

---

## 2. Solution

Our framework consists of five tightly integrated modules:

| Module      | Purpose                              | Key Mechanism                                         | Benefit                                                |
| ----------- | ------------------------------------ | ----------------------------------------------------- | ------------------------------------------------------ |
| **MS-GAT**  | Interaction-aware anomaly detection  | Multi-scale graph attention modeling                  | ↓ False positives by 30%, better anomaly localization  |
| **RL-DCAT** | Dynamic camera resource allocation   | Reinforcement learning with PPO controller            | ↓ Computational cost by 40%, ↑ recall by 15%           |
| **STICL**   | Generalization to rare events        | Inverse contrastive learning with anomaly memory bank | ↑ Rare anomaly recall by 25%                           |
| **NEBE**    | Low-latency motion anomaly detection | LIF spiking neural network with DVS input             | ↓ Detection latency by 60%, ↑ memory efficiency by 48% |
| **GBS-MFA** | Few-shot anomaly synthesis           | cGAN + meta-learning (MAML)                           | ↑ Generalization by 35%                                |

---

## 3. Results & Benchmarks

Evaluated on **UCF-Crime, ShanghaiTech, and Avenue** datasets, the framework achieved:

| Metric                       | Result              | Improvement                     |
| ---------------------------- | ------------------- | ------------------------------- |
| **Aggregate Accuracy**       | 93.7%               | +3.5% over Method25             |
| **Real-time Adaptability**   | 98.3%               | Enabled by RL-DCAT + NEBE       |
| **Computational Efficiency** | +50.2%              | Reduced overhead significantly  |
| **False Positive Rate**      | 4.5% (ShanghaiTech) | ↓ 63.4% vs Method3              |
| **Rare Anomaly Recall**      | 87.3% (Avenue)      | +15.2% over Method3             |
| **Frame Rate**               | 105 FPS (Multi-Cam) | vs. 92 FPS baseline             |
| **Inference Time**           | 9.2 ms/frame        | Efficient for real-time systems |

---

## 4. Future Scope

* **Self-Supervised Learning** to minimize labeled data requirements.
* **Audio-Visual Fusion** for contextual anomaly detection.
* **Adversarial Robustness** under varied environmental conditions.
* **Neuromorphic Hardware Co-Design** for further latency and energy gains.
* **Full Autonomy** for minimal human intervention.

---

## 5. Installation & Usage

```bash
# Clone repository
git clone https://github.com/yourusername/multi-camera-anomaly-detection.git
cd multi-camera-anomaly-detection

# Install dependencies
pip install -r requirements.txt

# Run training or inference
python main.py --config configs/config.yaml
```

> **Note:** Ensure you have access to UCF-Crime, ShanghaiTech, and Avenue datasets before running.

---

## 6. Dataset Links

* **UCF-Crime** – [Dataset Link](https://www.crcv.ucf.edu/projects/real-world/)
* **ShanghaiTech** – [Dataset Link](https://www.cse.cuhk.edu.hk/leojia/projects/detectabnormal/dataset.html)
* **Avenue** – [Dataset Link](https://svip-lab.github.io/dataset/campus_dataset.html)

---

## 7. References & Acknowledgements

This implementation is **based on and inspired by the open-access research paper**:

> Sai Babu Veesam, B. Tarakeswara Rao, Zarina Begum, R. S. M. Lakshmi Patibandla,
> Arvin Arun Dcosta, Shonak Bansal, Krishna Prakash, Mohammad Rashed Iqbal Faruque,
> & K. S. Al-mugren.
> *Multi-Camera Spatiotemporal Deep Learning Framework for Real-Time Abnormal Behavior Detection in Dense Urban Environments.* (2025).
> DOI/Link: [Insert DOI or Link]

We have adapted and paraphrased the problem statement, methodology descriptions, and performance metrics for educational and implementation purposes while retaining attribution to the original authors.

---

## 8. License

This project is licensed under the **MIT License**:



## 9. Citation

If you use this work in your research, please cite:

```bibtex
@article{multi_camera_anomaly_2025,
  title={Multi-Camera Spatiotemporal Deep Learning Framework for Real-Time Abnormal Behavior Detection in Dense Urban Environments},
  author={Veesam, Sai Babu and Rao, B. Tarakeswara and Begum, Zarina and Patibandla, R. S. M. Lakshmi and Dcosta, Arvin Arun and Bansal, Shonak and Prakash, Krishna and Faruque, Mohammad Rashed Iqbal and Al-mugren, K. S.},
  year={2025}
}
```




## References & Acknowledgements

This work is based on the open-access research paper:

> Sai Babu Veesam, B. Tarakeswara Rao, Zarina Begum, R. S. M. Lakshmi Patibandla,  
> Arvin Arun Dcosta, Shonak Bansal, Krishna Prakash, Mohammad Rashed Iqbal Faruque,  
> & K. S. Al-mugren.  
> *Multi-Camera Spatiotemporal Deep Learning Framework for Real-Time Abnormal Behavior Detection in Dense Urban Environments.* (2025).  
> DOI: [https://doi.org/10.1038/s41598-025-12388-7](https://doi.org/10.1038/s41598-025-12388-7)




