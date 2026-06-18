package com.equifax.frauddetection.controller;

import com.equifax.frauddetection.util.JwtUtil;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/auth")
public class AuthController {

    private final JwtUtil jwtUtil;

    public AuthController(JwtUtil jwtUtil) {
        this.jwtUtil = jwtUtil;
    }

    @PostMapping("/login")
    public Map<String, String> login(@RequestParam String username, @RequestParam String password) {
        // In a real application, validate username and password from database.
        // For demonstration, we allow any login and issue a JWT.
        Map<String, String> response = new HashMap<>();
        if ("admin".equals(username) && "password".equals(password)) {
            response.put("token", jwtUtil.generateToken(username));
        } else {
            response.put("error", "Invalid credentials. Use admin / password");
        }
        return response;
    }
}
