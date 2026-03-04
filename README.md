# Event Driven Data Engine

This project is part of my journey learning software engineering and event-driven architectures using Python.

Instead of starting with small scripts, I became curious about how real systems process events, distribute work across workers, and generate structured data.  
So I started experimenting with a small **event-driven engine** that monitors filesystem activity and processes events through a modular pipeline.

---

## How this project started

The origin of this project was actually very simple.

I needed a way to organize files for audio and video production.  
My initial goal was to create a YouTube channel to publish music experiments and radio-style mixes.

Over time I accumulated a large number of audio files and samples, and I wanted a faster way to:

- organize audio files
- process recordings
- standardize outputs for radio-style mixes
- prepare datasets from my own audio experiments

At the beginning the idea was just automation.

But while exploring solutions and discussing ideas with ChatGPT, the project slowly evolved into something more interesting: a small **event-driven processing engine**.

The original idea was simple:

> What if I could drop audio files into a folder and have the system process everything automatically?

Something like **"one click mastering and organization"**.

---

## My Background

I come from a creative background, not software engineering.

Most of my experience before this project was with:

- music production
- audio mixing
- video and image editing

Using tools such as:

- Fruity Loops (FL Studio)
- Ableton Live
- video editing tools
- sound design workflows

I started learning Python very recently — about **three weeks ago** — while also beginning studies in **Artificial Intelligence**.

This project became my way of learning by building something real.

Surprisingly, after about a week of experimentation, I had a basic engine running.

At that moment I realized this might become something more than just a file organizer.

---

## Project Goal

The main goal of this project is to understand how **event-based systems** work internally.

The engine monitors filesystem activity and converts file events into structured messages that can be processed by different components.

This allows experimentation with:

- event pipelines
- concurrent workers
- logging and metrics
- structured data generation
- dataset creation for machine learning

---

## Current Architecture

The system currently contains several independent modules.

**Watcher**  
Monitors filesystem activity and detects new files.

**EventBus**  
Distributes events internally between system components.

**WorkerPool**  
Processes tasks concurrently.

**Metrics Module**  
Tracks queue size and processing statistics.

**Dataset Builder**  
Transforms engine events into structured datasets using Parquet.

---

## System Flow
