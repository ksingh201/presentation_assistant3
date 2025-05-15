# Recovery Guide

This document provides detailed recovery procedures and troubleshooting steps for the Presentation Assistant.

## Common Issues and Solutions

### 1. Slide Detection Issues

**Symptoms:**
- Slide index stuck at 1
- No slide changes detected
- Incorrect slide index mapping

**Recovery Steps:**
1. Check if the slide detector is running:
   ```bash
   curl http://localhost:8765/slide-change
   ```
2. Verify Google Slides URL in `.env` file
3. Check browser console for any errors
4. Restart the application

### 2. Speaker Notes Not Loading

**Symptoms:**
- Empty speaker notes
- "No notes found" messages
- Missing narration

**Recovery Steps:**
1. Verify Google service account permissions
2. Check if speaker notes exist in the presentation
3. Run debug script:
   ```bash
   python temp_script_debug.py
   ```
4. Verify credentials file exists and is valid

### 3. Speech Recognition Issues

**Symptoms:**
- "NO" responses not detected
- Transcription errors
- No response to questions

**Recovery Steps:**
1. Check microphone permissions
2. Verify OpenAI API key
3. Check audio device settings
4. Run test recording:
   ```python
   from stt_service import STTService
   stt = STTService()
   response = await stt.listen(5.0)
   print(f"Transcription: {response}")
   ```

### 4. TTS (Text-to-Speech) Issues

**Symptoms:**
- No audio output
- Delayed narration
- Audio quality issues

**Recovery Steps:**
1. Check system audio settings
2. Verify audio device is working
3. Test TTS directly:
   ```python
   from tts_service import TTSService
   tts = TTSService()
   tts.speak("Test message")
   ```

## System Recovery

### Complete System Reset

1. Stop all running processes:
   ```bash
   pkill -f "python main.py"
   ```

2. Clear temporary files:
   ```bash
   rm -f *.wav *.mp3
   ```

3. Reset environment:
   ```bash
   deactivate  # If in virtual environment
   rm -rf .venv
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. Verify configuration:
   - Check `.env` file
   - Verify `google_credentials.json`
   - Test API connections

### Data Recovery

1. Speaker Notes:
   - Backup notes from Google Slides
   - Export to local file if needed
   - Use `slides_service.py` to verify access

2. Configuration:
   - Backup `.env` file
   - Save API keys securely
   - Document custom settings

## Performance Optimization

### Memory Issues

**Symptoms:**
- High memory usage
- Slow response times
- Audio buffering

**Solutions:**
1. Clear audio cache:
   ```bash
   rm -f *.wav *.mp3
   ```
2. Reduce audio buffer size in `tts_service.py`
3. Implement audio cleanup after use

### Network Issues

**Symptoms:**
- API timeouts
- Slow slide detection
- Delayed responses

**Solutions:**
1. Check internet connection
2. Verify API endpoints
3. Implement retry logic
4. Cache frequently used data

## Security Recovery

### API Key Compromise

1. Immediately revoke compromised keys
2. Generate new keys
3. Update `.env` file
4. Verify all services work with new keys

### Credential Issues

1. Regenerate Google service account credentials
2. Update `google_credentials.json`
3. Verify Slides API access
4. Test with new credentials

## Backup Procedures

### Regular Backups

1. Configuration:
   ```bash
   cp .env .env.backup
   cp google_credentials.json google_credentials.json.backup
   ```

2. Code:
   ```bash
   git add .
   git commit -m "Backup $(date +%Y-%m-%d)"
   ```

3. Speaker Notes:
   - Export from Google Slides
   - Save as local file
   - Document any custom formatting

### Restore from Backup

1. Configuration:
   ```bash
   cp .env.backup .env
   cp google_credentials.json.backup google_credentials.json
   ```

2. Code:
   ```bash
   git checkout <backup-commit>
   ```

3. Speaker Notes:
   - Import to Google Slides
   - Verify formatting
   - Test narration

## Monitoring and Logging

### Enable Debug Logging

1. Set environment variable:
   ```bash
   export DEBUG=1
   ```

2. Check logs:
   ```bash
   tail -f debug.log
   ```

### Performance Monitoring

1. Monitor memory usage:
   ```bash
   ps aux | grep python
   ```

2. Check API response times:
   ```bash
   curl -w "%{time_total}\n" http://localhost:8765/slide-change
   ```

## Contact and Support

For additional support:
1. Check GitHub issues
2. Contact development team
3. Review documentation
4. Submit bug reports

## Version History

- v1.0.0: Initial release
- v1.1.0: Added Q&A functionality
- v1.2.0: Improved speech recognition
- v1.3.0: Enhanced error recovery
- v1.4.0: Simplified slide detection and TTS integration

## Recent Changes and Improvements

### Slide Detection Improvements
- Removed dependency on separate web server for slide detection
- Integrated slide detection directly into main application
- Improved handling of slide ID mapping
- Added support for real-time slide change detection

### TTS Integration
- Simplified TTS service integration
- Improved audio playback handling
- Enhanced error handling for TTS operations
- Added support for continuous narration

### Code Structure
- Streamlined main application flow
- Improved error handling and logging
- Enhanced configuration management
- Better separation of concerns

### Performance Optimizations
- Reduced memory usage
- Improved response times
- Enhanced audio buffering
- Better resource management

## Future Improvements

1. Implement automatic backup
2. Add health monitoring
3. Improve error reporting
4. Enhance recovery automation 