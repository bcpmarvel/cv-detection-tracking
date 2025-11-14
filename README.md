# Real-Time Object Detection & Tracking

High-performance video analytics system for real-time object detection and multi-object tracking, optimized for edge deployment.

## Project Overview

This system processes live video streams (webcam/files) to detect and track multiple objects in real-time. Built for production use cases in surveillance, retail analytics, and smart infrastructure monitoring.

**Core Capabilities:**
- Real-time object detection with YOLOv8
- Persistent multi-object tracking across frames
- Zone-based analytics (counting, dwell time, violations)
- REST/WebSocket API for integration
- Optimized for resource-constrained environments

## Architecture
```
Video Input → Detection → Tracking → Analytics → Output/API
     ↓           ↓           ↓          ↓           ↓
  Webcam/     YOLOv8    BoT-SORT   Counters   Display/
   File                            Zones      Stream
```

**Processing Pipeline:**
1. **Capture**: Video frames from source (webcam/file)
2. **Detect**: YOLOv8n identifies objects with bounding boxes
3. **Track**: BoT-SORT maintains object IDs across frames
4. **Analyze**: Zone monitoring, counting, dwell time calculation
5. **Output**: Annotated video stream or REST/WebSocket API

## Technology Stack

### Core Detection & Tracking
- **YOLOv8n** - Object detection model (Ultralytics)
- **BoT-SORT** - Multi-object tracking algorithm
- **PyTorch 2.5** - Deep learning framework with MPS backend
- **Supervision** - Video annotation and tracking utilities

### Computer Vision
- **OpenCV** - Video I/O and frame processing
- **NumPy** - Numerical operations on frames
- **Pillow** - Image manipulation

### API & Services
- **FastAPI** - REST API server
- **WebSockets** - Real-time video streaming
- **Uvicorn** - ASGI server

### Development
- **Pydantic** - Configuration management
- **pytest** - Testing framework
- **Ruff** - Linting and formatting

## Key Technical Decisions

**Why YOLOv8n (nano)?**
- Fastest YOLO variant (30+ FPS on CPU)
- Good accuracy/speed tradeoff for real-time use
- 3MB model size suitable for edge deployment

**Why BoT-SORT?**
- State-of-art tracking accuracy
- Built into Ultralytics (no extra dependencies)
- Handles occlusions and re-identification

**Why PyTorch MPS?**
- Native M1/M2 GPU acceleration
- 2-3x faster than CPU inference
- No CUDA dependency

**Why FastAPI?**
- Modern async Python framework
- WebSocket support for streaming
- Auto-generated OpenAPI docs

## Performance Targets

| Metric | Target | Hardware |
|--------|--------|----------|
| FPS | 30+ | M1 MacBook @ 720p |
| Latency | <50ms | Per-frame inference |
| Memory | <200MB | Runtime overhead |
| Startup | <3s | Model loading |

## Use Cases

**Surveillance & Security**
- Real-time threat detection
- Perimeter monitoring
- Access control validation

**Retail Analytics**
- Customer traffic counting
- Queue length monitoring
- Dwell time analysis

**Smart Infrastructure**
- Traffic flow monitoring
- Occupancy detection
- Safety compliance

## Implementation Components

### `src/config.py`
Configuration management with Pydantic settings. Handles model paths, thresholds, device selection, and runtime parameters.

### `src/detect.py`
Main detection pipeline. Loads video source, runs inference, visualizes results. Supports CLI arguments for source selection and output options.

### `src/tracker.py`
Multi-object tracking wrapper around BoT-SORT. Maintains object IDs across frames, handles occlusions and re-identification.

### `src/analytics.py`
Zone-based analytics engine. Tracks object counts, dwell times, zone violations, and generates metrics.

### `src/api.py`
FastAPI server exposing REST endpoints and WebSocket streams. Enables programmatic access to detection/tracking capabilities.

## Development Approach

**Phase 1: Core Detection** (Current)
- Basic YOLOv8 inference on video
- Display with bounding boxes
- FPS monitoring

**Phase 2: Tracking**
- Add BoT-SORT tracker
- Persistent object IDs
- Track visualization

**Phase 3: Analytics**
- Zone definition
- Object counting
- Dwell time calculation

**Phase 4: API**
- FastAPI REST endpoints
- WebSocket streaming
- API documentation

## Hardware Optimization

**M1/M2 MacBooks:**
- PyTorch MPS backend (GPU acceleration)
- Automatic batch processing
- Efficient memory management

**Intel CPUs:**
- OpenVINO conversion (future)
- INT8 quantization
- Multi-threading

**Edge Devices:**
- ONNX export for portability
- TensorRT for NVIDIA
- CoreML for Apple Silicon

## Future Enhancements

- [ ] Multi-camera synchronization
- [ ] Cloud deployment (Docker/K8s)
- [ ] Custom object classes (fine-tuning)
- [ ] Prometheus metrics export
- [ ] Video storage integration
- [ ] Alert/notification system

## Key Metrics for Portfolio

**Technical Depth:**
- Real-time processing (30+ FPS)
- Production-ready code (type hints, tests, docs)
- Multiple interfaces (CLI + API)

**Engineering Quality:**
- Clean architecture (separation of concerns)
- Configurable (Pydantic settings)
- Deployable (Docker support)

**Relevance to Role:**
- Video analytics (Gorilla's core product)
- Edge optimization (Intel partnership)
- Production deployment (FastAPI service)