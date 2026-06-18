package com.equifax.frauddetection.service;

import com.equifax.frauddetection.model.Transaction;
import com.equifax.frauddetection.repository.TransactionRepository;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import java.time.LocalDateTime;
import java.util.Map;

@Service
public class TransactionService {

    private final TransactionRepository transactionRepository;
    private final RestClient restClient;

    public TransactionService(TransactionRepository transactionRepository) {
        this.transactionRepository = transactionRepository;
        this.restClient = RestClient.create("http://127.0.0.1:8000");
    }

    public Transaction processTransaction(Transaction transaction) {
        // Set timestamp if not present
        if (transaction.getTimestamp() == null) {
            transaction.setTimestamp(LocalDateTime.now());
        }

        // Call Python AI Service for evaluation
        try {
            Map<String, Object> aiResponse = restClient.post()
                    .uri("/evaluate-fraud")
                    .body(transaction)
                    .retrieve()
                    .body(Map.class);

            if (aiResponse != null) {
                Boolean isFraud = (Boolean) aiResponse.get("isFraud");
                String explanation = (String) aiResponse.get("explanation");
                transaction.setIsFraud(isFraud);
                transaction.setXaiExplanation(explanation);
            }
        } catch (Exception e) {
            System.err.println("Failed to reach Python AI Service: " + e.getMessage());
            transaction.setIsFraud(false);
            transaction.setXaiExplanation("AI Service Unavailable");
        }

        // Save transaction to database
        return transactionRepository.save(transaction);
    }
}
