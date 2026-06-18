package com.equifax.frauddetection.model;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

@Entity
@Data
public class Transaction {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String userId;
    private Double amount;
    private String location;
    private LocalDateTime timestamp;
    private Double distanceToPrevious; // Distance from previous transaction location in miles
    private Boolean isFraud;
    
    @Column(length = 1000)
    private String xaiExplanation;
}
